from llama_index.core import Settings
from llama_index.core.settings import _Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from app.core.config import settings
from llama_index.core.node_parser import SentenceSplitter

from app.chat.constants import (
    NODE_PARSER_CHUNK_OVERLAP,
    NODE_PARSER_CHUNK_SIZE,
)

def _setup_llama_index_settings() -> _Settings:
    Settings.llm = OpenAI(
        model=settings.OPENAI_CHAT_LLM_NAME,
        api_key=settings.OPENAI_API_KEY
    )
    Settings.embed_model = OpenAIEmbedding(
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model_type=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL,
        api_key=settings.OPENAI_API_KEY,
    )
    Settings.node_parser = SentenceSplitter(
        chunk_size=NODE_PARSER_CHUNK_SIZE,
        chunk_overlap=NODE_PARSER_CHUNK_OVERLAP,
    )
    return Settings
