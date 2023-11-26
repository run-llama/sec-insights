from typing import Dict, List, Optional
import logging
from pathlib import Path
from datetime import datetime
import s3fs
from fsspec.asyn import AsyncFileSystem
from llama_index import (
    ServiceContext,
    VectorStoreIndex,
    StorageContext,
    load_indices_from_storage,
)
from llama_index.vector_stores.types import VectorStore
from tempfile import TemporaryDirectory
import requests
import nest_asyncio
from datetime import timedelta
from cachetools import cached, TTLCache
from llama_index.readers.file.docs_reader import PDFReader
from llama_index.schema import Document as LlamaIndexDocument
from llama_index.agent import OpenAIAgent
from llama_index.llms import ChatMessage, OpenAI
from llama_index.embeddings.openai import (
    OpenAIEmbedding,
    OpenAIEmbeddingMode,
    OpenAIEmbeddingModelType,
)
from llama_index.llms.base import MessageRole
from llama_index.callbacks.base import BaseCallbackHandler, CallbackManager
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.indices.query.base import BaseQueryEngine
from llama_index.vector_stores.types import (
    MetadataFilters,
    ExactMatchFilter,
)
from llama_index.node_parser import SentenceSplitter
from app.core.config import settings
from app.schema import (
    Message as MessageSchema,
    Document as DocumentSchema,
    Conversation as ConversationSchema,
    DocumentMetadataKeysEnum,
    SecDocumentMetadata,
)
from app.models.db import MessageRoleEnum, MessageStatusEnum
from app.chat.constants import (
    DB_DOC_ID_KEY,
    SYSTEM_MESSAGE,
    NODE_PARSER_CHUNK_OVERLAP,
    NODE_PARSER_CHUNK_SIZE,
)
from app.chat.tools import get_api_query_engine_tool
from app.chat.utils import build_title_for_document
from app.chat.pg_vector import get_vector_store_singleton
from app.chat.qa_response_synth import get_custom_response_synth


logger = logging.getLogger(__name__)


logger.info("Applying nested asyncio patch")
nest_asyncio.apply()

OPENAI_TOOL_LLM_NAME = "gpt-3.5-turbo-0613"
OPENAI_CHAT_LLM_NAME = "gpt-3.5-turbo-0613"


def get_s3_fs() -> AsyncFileSystem:
    s3 = s3fs.S3FileSystem(
        key=settings.AWS_KEY,
        secret=settings.AWS_SECRET,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )
    if not (settings.RENDER or s3.exists(settings.S3_BUCKET_NAME)):
        s3.mkdir(settings.S3_BUCKET_NAME)
    return s3


def fetch_and_read_document(
    document: DocumentSchema,
) -> List[LlamaIndexDocument]:
    # Super hacky approach to get this to feature complete on time.
    # TODO: Come up with better abstractions for this and the other methods in this module.
    with TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / f"{str(document.id)}.pdf"
        with open(temp_file_path, "wb") as temp_file:
            with requests.get(document.url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
            temp_file.seek(0)
            reader = PDFReader()
            return reader.load_data(
                temp_file_path, extra_info={DB_DOC_ID_KEY: str(document.id)}
            )


def build_description_for_document(document: DocumentSchema) -> str:
    if DocumentMetadataKeysEnum.SEC_DOCUMENT in document.metadata_map:
        sec_metadata = SecDocumentMetadata.parse_obj(
            document.metadata_map[DocumentMetadataKeysEnum.SEC_DOCUMENT]
        )
        time_period = (
            f"{sec_metadata.year} Q{sec_metadata.quarter}"
            if sec_metadata.quarter
            else str(sec_metadata.year)
        )
        return f"A SEC {sec_metadata.doc_type.value} filing describing the financials of {sec_metadata.company_name} ({sec_metadata.company_ticker}) for the {time_period} time period."
    return "A document containing useful information that the user pre-selected to discuss with the assistant."


def index_to_query_engine(doc_id: str, index: VectorStoreIndex) -> BaseQueryEngine:
    filters = MetadataFilters(
        filters=[ExactMatchFilter(key=DB_DOC_ID_KEY, value=doc_id)]
    )
    kwargs = {"similarity_top_k": 3, "filters": filters}
    return index.as_query_engine(**kwargs)


@cached(
    TTLCache(maxsize=10, ttl=timedelta(minutes=5).total_seconds()),
    key=lambda *args, **kwargs: "global_storage_context",
)
def get_storage_context(
    persist_dir: str, vector_store: VectorStore, fs: Optional[AsyncFileSystem] = None
) -> StorageContext:
    logger.info("Creating new storage context.")
    return StorageContext.from_defaults(
        persist_dir=persist_dir, vector_store=vector_store, fs=fs
    )


async def build_doc_id_to_index_map(
    service_context: ServiceContext,
    documents: List[DocumentSchema],
    fs: Optional[AsyncFileSystem] = None,
) -> Dict[str, VectorStoreIndex]:
    persist_dir = f"{settings.S3_BUCKET_NAME}"

    vector_store = await get_vector_store_singleton()
    try:
        try:
            storage_context = get_storage_context(persist_dir, vector_store, fs=fs)
        except FileNotFoundError:
            logger.info(
                "Could not find storage context in S3. Creating new storage context."
            )
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store, fs=fs
            )
            storage_context.persist(persist_dir=persist_dir, fs=fs)
        index_ids = [str(doc.id) for doc in documents]
        indices = load_indices_from_storage(
            storage_context,
            index_ids=index_ids,
            service_context=service_context,
        )
        doc_id_to_index = dict(zip(index_ids, indices))
        logger.debug("Loaded indices from storage.")
    except ValueError:
        logger.error(
            "Failed to load indices from storage. Creating new indices. "
            "If you're running the seed_db script, this is normal and expected."
        )
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir, vector_store=vector_store, fs=fs
        )
        doc_id_to_index = {}
        for doc in documents:
            llama_index_docs = fetch_and_read_document(doc)
            storage_context.docstore.add_documents(llama_index_docs)
            index = VectorStoreIndex.from_documents(
                llama_index_docs,
                storage_context=storage_context,
                service_context=service_context,
            )
            index.set_index_id(str(doc.id))
            index.storage_context.persist(persist_dir=persist_dir, fs=fs)
            doc_id_to_index[str(doc.id)] = index
    return doc_id_to_index


def get_chat_history(
    chat_messages: List[MessageSchema],
) -> List[ChatMessage]:
    """
    Given a list of chat messages, return a list of ChatMessage instances.

    Failed chat messages are filtered out and then the remaining ones are
    sorted by created_at.
    """
    # pre-process chat messages
    chat_messages = [
        m
        for m in chat_messages
        if m.content.strip() and m.status == MessageStatusEnum.SUCCESS
    ]
    # TODO: could be a source of high CPU utilization
    chat_messages = sorted(chat_messages, key=lambda m: m.created_at)

    chat_history = []
    for message in chat_messages:
        role = (
            MessageRole.ASSISTANT
            if message.role == MessageRoleEnum.assistant
            else MessageRole.USER
        )
        chat_history.append(ChatMessage(content=message.content, role=role))

    return chat_history


def get_tool_service_context(
    callback_handlers: List[BaseCallbackHandler],
) -> ServiceContext:
    llm = OpenAI(
        temperature=0,
        model=OPENAI_TOOL_LLM_NAME,
        streaming=False,
        api_key=settings.OPENAI_API_KEY,
    )
    callback_manager = CallbackManager(callback_handlers)
    embedding_model = OpenAIEmbedding(
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model_type=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        api_key=settings.OPENAI_API_KEY,
    )
    # Use a smaller chunk size to retrieve more granular results
    node_parser = SentenceSplitter.from_defaults(
        chunk_size=NODE_PARSER_CHUNK_SIZE,
        chunk_overlap=NODE_PARSER_CHUNK_OVERLAP,
        callback_manager=callback_manager,
    )
    service_context = ServiceContext.from_defaults(
        callback_manager=callback_manager,
        llm=llm,
        embed_model=embedding_model,
        node_parser=node_parser,
    )
    return service_context


async def get_chat_engine(
    callback_handler: BaseCallbackHandler,
    conversation: ConversationSchema,
) -> OpenAIAgent:
    service_context = get_tool_service_context([callback_handler])
    s3_fs = get_s3_fs()
    doc_id_to_index = await build_doc_id_to_index_map(
        service_context, conversation.documents, fs=s3_fs
    )
    id_to_doc: Dict[str, DocumentSchema] = {
        str(doc.id): doc for doc in conversation.documents
    }

    vector_query_engine_tools = [
        QueryEngineTool(
            query_engine=index_to_query_engine(doc_id, index),
            metadata=ToolMetadata(
                name=doc_id,
                description=build_description_for_document(id_to_doc[doc_id]),
            ),
        )
        for doc_id, index in doc_id_to_index.items()
    ]

    response_synth = get_custom_response_synth(service_context, conversation.documents)

    qualitative_question_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=vector_query_engine_tools,
        service_context=service_context,
        response_synthesizer=response_synth,
        verbose=settings.VERBOSE,
        use_async=True,
    )

    api_query_engine_tools = [
        get_api_query_engine_tool(doc, service_context)
        for doc in conversation.documents
        if DocumentMetadataKeysEnum.SEC_DOCUMENT in doc.metadata_map
    ]

    quantitative_question_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=api_query_engine_tools,
        service_context=service_context,
        response_synthesizer=response_synth,
        verbose=settings.VERBOSE,
        use_async=True,
    )

    top_level_sub_tools = [
        QueryEngineTool(
            query_engine=qualitative_question_engine,
            metadata=ToolMetadata(
                name="qualitative_question_engine",
                description="""
A query engine that can answer qualitative questions about a set of SEC financial documents that the user pre-selected for the conversation.
Any questions about company-related headwinds, tailwinds, risks, sentiments, or administrative information should be asked here.
""".strip(),
            ),
        ),
        QueryEngineTool(
            query_engine=quantitative_question_engine,
            metadata=ToolMetadata(
                name="quantitative_question_engine",
                description="""
A query engine that can answer quantitative questions about a set of SEC financial documents that the user pre-selected for the conversation.
Any questions about company-related financials or other metrics should be asked here.
""".strip(),
            ),
        ),
    ]

    chat_llm = OpenAI(
        temperature=0,
        model=OPENAI_CHAT_LLM_NAME,
        streaming=True,
        api_key=settings.OPENAI_API_KEY,
    )
    chat_messages: List[MessageSchema] = conversation.messages
    chat_history = get_chat_history(chat_messages)
    logger.debug("Chat history: %s", chat_history)

    if conversation.documents:
        doc_titles = "\n".join(
            "- " + build_title_for_document(doc) for doc in conversation.documents
        )
    else:
        doc_titles = "No documents selected."

    curr_date = datetime.utcnow().strftime("%Y-%m-%d")
    chat_engine = OpenAIAgent.from_tools(
        tools=top_level_sub_tools,
        llm=chat_llm,
        chat_history=chat_history,
        verbose=settings.VERBOSE,
        system_prompt=SYSTEM_MESSAGE.format(doc_titles=doc_titles, curr_date=curr_date),
        callback_manager=service_context.callback_manager,
        max_function_calls=3,
    )

    return chat_engine
