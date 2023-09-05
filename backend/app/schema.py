"""
Pydantic Schemas for the API
"""
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import List, Optional, Dict, Union, Any
from uuid import UUID
from datetime import datetime
from llama_index.schema import BaseNode, NodeWithScore
from llama_index.callbacks.schema import EventPayload
from llama_index.query_engine.sub_question_query_engine import SubQuestionAnswerPair
from app.models.db import (
    MessageRoleEnum,
    MessageStatusEnum,
    MessageSubProcessSourceEnum,
    MessageSubProcessStatusEnum,
)
from app.chat.constants import DB_DOC_ID_KEY


def build_uuid_validator(*field_names: str):
    return validator(*field_names)(lambda x: str(x) if x else x)


class Base(BaseModel):
    id: Optional[UUID] = Field(None, description="Unique identifier")
    created_at: Optional[datetime] = Field(None, description="Creation datetime")
    updated_at: Optional[datetime] = Field(None, description="Update datetime")

    class Config:
        orm_mode = True


class BaseMetadataObject(BaseModel):
    class Config:
        orm_mode = True


class Citation(BaseMetadataObject):
    document_id: UUID
    text: str
    page_number: int
    score: Optional[float]

    @validator("document_id")
    def validate_document_id(cls, value):
        if value:
            return str(value)
        return value

    @classmethod
    def from_node(cls, node_w_score: NodeWithScore) -> "Citation":
        node: BaseNode = node_w_score.node
        page_number = int(node.source_node.metadata["page_label"])
        document_id = node.source_node.metadata[DB_DOC_ID_KEY]
        return cls(
            document_id=document_id,
            text=node.get_content(),
            page_number=page_number,
            score=node_w_score.score,
        )


class QuestionAnswerPair(BaseMetadataObject):
    """
    A question-answer pair that is used to store the sub-questions and answers
    """

    question: str
    answer: Optional[str]
    citations: Optional[List[Citation]] = None

    @classmethod
    def from_sub_question_answer_pair(
        cls, sub_question_answer_pair: SubQuestionAnswerPair
    ):
        if sub_question_answer_pair.sources is None:
            citations = None
        else:
            citations = [
                Citation.from_node(node_w_score)
                for node_w_score in sub_question_answer_pair.sources
                if node_w_score.node.source_node is not None
                and DB_DOC_ID_KEY in node_w_score.node.source_node.metadata
            ]
        citations = citations or None
        return cls(
            question=sub_question_answer_pair.sub_q.sub_question,
            answer=sub_question_answer_pair.answer,
            citations=citations,
        )


# later will be Union[QuestionAnswerPair, more to add later... ]
class SubProcessMetadataKeysEnum(str, Enum):
    SUB_QUESTION = EventPayload.SUB_QUESTION.value


# keeping the typing pretty loose here, in case there are changes to the metadata data formats.
SubProcessMetadataMap = Dict[Union[SubProcessMetadataKeysEnum, str], Any]


class MessageSubProcess(Base):
    message_id: UUID
    source: MessageSubProcessSourceEnum
    status: MessageSubProcessStatusEnum
    metadata_map: Optional[SubProcessMetadataMap]


class Message(Base):
    conversation_id: UUID
    content: str
    role: MessageRoleEnum
    status: MessageStatusEnum
    sub_processes: List[MessageSubProcess]


class UserMessageCreate(BaseModel):
    content: str


class DocumentMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_document"


class SecDocumentTypeEnum(str, Enum):
    """
    Enum for the type of sec document
    """

    TEN_K = "10-K"
    TEN_Q = "10-Q"


class SecDocumentMetadata(BaseModel):
    """
    Metadata for a document that is a sec document
    """

    company_name: str
    company_ticker: str
    doc_type: SecDocumentTypeEnum
    year: int
    quarter: Optional[int]
    accession_number: Optional[str]
    cik: Optional[str]
    period_of_report_date: Optional[datetime]
    filed_as_of_date: Optional[datetime]
    date_as_of_change: Optional[datetime]


DocumentMetadataMap = Dict[Union[DocumentMetadataKeysEnum, str], Any]


class Document(Base):
    url: str
    metadata_map: Optional[DocumentMetadataMap] = None


class Conversation(Base):
    messages: List[Message]
    documents: List[Document]


class ConversationCreate(BaseModel):
    document_ids: List[UUID]
