from typing import Optional, cast, Sequence, List
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db import Conversation, Message, Document, ConversationDocument
from app import schema
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert


async def fetch_conversation_with_messages(
    db: AsyncSession, conversation_id: str
) -> Optional[schema.Conversation]:
    """
    Fetch a conversation with its messages + messagesubprocesses
    return None if the conversation with the given id does not exist
    """
    # Eagerly load required relationships
    stmt = (
        select(Conversation)
        .options(joinedload(Conversation.messages).subqueryload(Message.sub_processes))
        .options(
            joinedload(Conversation.conversation_documents).subqueryload(
                ConversationDocument.document
            )
        )
        .where(Conversation.id == conversation_id)
    )

    result = await db.execute(stmt)  # execute the statement
    conversation = result.scalars().first()  # get the first result
    if conversation is not None:
        convo_dict = {
            **conversation.__dict__,
            "documents": [
                convo_doc.document for convo_doc in conversation.conversation_documents
            ],
        }
        return schema.Conversation(**convo_dict)
    return None


async def create_conversation(
    db: AsyncSession, convo_payload: schema.ConversationCreate
) -> schema.Conversation:
    conversation = Conversation()
    convo_doc_db_objects = [
        ConversationDocument(document_id=doc_id, conversation=conversation)
        for doc_id in convo_payload.document_ids
    ]
    db.add(conversation)
    db.add_all(convo_doc_db_objects)
    await db.commit()
    await db.refresh(conversation)
    return await fetch_conversation_with_messages(db, conversation.id)


async def delete_conversation(db: AsyncSession, conversation_id: str) -> bool:
    stmt = delete(Conversation).where(Conversation.id == conversation_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def fetch_message_with_sub_processes(
    db: AsyncSession, message_id: str
) -> Optional[schema.Message]:
    """
    Fetch a message with its sub processes
    return None if the message with the given id does not exist
    """
    # Eagerly load required relationships
    stmt = (
        select(Message)
        .options(joinedload(Message.sub_processes))
        .where(Message.id == message_id)
    )
    result = await db.execute(stmt)  # execute the statement
    message = result.scalars().first()  # get the first result
    if message is not None:
        return schema.Message.from_orm(message)
    return None


async def fetch_documents(
    db: AsyncSession,
    id: Optional[str] = None,
    ids: Optional[List[str]] = None,
    url: Optional[str] = None,
    limit: Optional[int] = None,
) -> Optional[Sequence[schema.Document]]:
    """
    Fetch a document by its url or id
    """

    stmt = select(Document)
    if id is not None:
        stmt = stmt.where(Document.id == id)
        limit = 1
    elif ids is not None:
        stmt = stmt.where(Document.id.in_(ids))
    if url is not None:
        stmt = stmt.where(Document.url == url)
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    documents = result.scalars().all()
    return [schema.Document.from_orm(doc) for doc in documents]


async def upsert_document_by_url(
    db: AsyncSession, document: schema.Document
) -> schema.Document:
    """
    Upsert a document
    """
    stmt = insert(Document).values(**document.dict(exclude_none=True))
    stmt = stmt.on_conflict_do_update(
        index_elements=[Document.url],
        set_=document.dict(include={"metadata_map"}),
    )
    stmt = stmt.returning(Document)
    result = await db.execute(stmt)
    upserted_doc = schema.Document.from_orm(result.scalars().first())
    await db.commit()
    return upserted_doc
