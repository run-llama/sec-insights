from typing import Dict, Any, Optional, List
import asyncio
import logging
from uuid import uuid4
from anyio import ClosedResourceError
from anyio.streams.memory import MemoryObjectSendStream

from llama_index.callbacks.base import BaseCallbackHandler
from llama_index.callbacks.schema import CBEventType, EventPayload
from llama_index.query_engine.sub_question_query_engine import SubQuestionAnswerPair
from llama_index.agent.openai_agent import StreamingAgentChatResponse
from pydantic import BaseModel
from guardrails import Guard
from guardrails.hub import RestrictToTopic, ToxicLanguage

from app import schema
from app.schema import SubProcessMetadataKeysEnum, SubProcessMetadataMap
from app.models.db import MessageSubProcessSourceEnum
from app.chat.engine import get_chat_engine

logger = logging.getLogger(__name__)

guard = Guard().use_many(
    # RestrictToTopic(
    #     valid_topics=["AI", "Language Models"],
    #     on_fail="exception"
    # ),  # Keeps responses on-topic
    ToxicLanguage(threshold=0.5, on_fail="exception")  # Blocks toxic content
)

class StreamedMessage(BaseModel):
    content: str


class StreamedMessageSubProcess(BaseModel):
    source: MessageSubProcessSourceEnum
    has_ended: bool
    event_id: str
    metadata_map: Optional[SubProcessMetadataMap] = None  # Explicit default


class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        send_chan: MemoryObjectSendStream,
    ):
        """Initialize the base callback handler."""
        # ignored_events = [CBEventType.CHUNKING, CBEventType.NODE_PARSING]
        ignored_events = [
            CBEventType.CHUNKING,
            CBEventType.NODE_PARSING,
            CBEventType.EMBEDDING,  # Ignore low-level events
            CBEventType.RETRIEVE,
            CBEventType.TEMPLATING,
        ]
        super().__init__(ignored_events, ignored_events)
        self._send_chan = send_chan
        self.response_complete = False

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> str:
        """Create the MessageSubProcess row for the event that started."""
        asyncio.create_task(
            self.async_on_event(
                event_type, payload, event_id, is_start_event=True, **kwargs
            )
        )

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Create the MessageSubProcess row for the event that completed."""
        asyncio.create_task(
            self.async_on_event(
                event_type, payload, event_id, is_start_event=False, **kwargs
            )
        )

    def get_metadata_from_event(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        is_start_event: bool = False,
    ) -> SubProcessMetadataMap:
        metadata_map = {}

        if (
            event_type == CBEventType.SUB_QUESTION
            and EventPayload.SUB_QUESTION in payload
        ):
            sub_q: SubQuestionAnswerPair = payload[EventPayload.SUB_QUESTION]
            metadata_map[
                SubProcessMetadataKeysEnum.SUB_QUESTION.value
            ] = schema.QuestionAnswerPair.from_sub_question_answer_pair(sub_q).dict()
        return metadata_map

    async def async_on_event(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        is_start_event: bool = False,
        **kwargs: Any,
    ) -> None:
        metadata_map = self.get_metadata_from_event(
            event_type, payload=payload, is_start_event=is_start_event
        )
        metadata_map = metadata_map or None
        source = MessageSubProcessSourceEnum[event_type.name]
        if self._send_chan._closed:
            logger.debug("Received event after send channel closed. Ignoring.")
            return
        try:
            await self._send_chan.send(
                StreamedMessageSubProcess(
                    source=source,
                    metadata_map=metadata_map,
                    event_id=event_id,
                    has_ended=not is_start_event,
                )
            )
            # if event_type in [CBEventType.SYNTHESIZE, CBEventType.LLM] and not is_start_event:
            #     self.response_complete = True
            if event_type == CBEventType.SYNTHESIZE and not is_start_event:
                self.response_complete = True
                logger.debug("Synthesis complete; stopping further events")
        except ClosedResourceError:
            logger.exception("Tried sending SubProcess event %s after channel was closed", f"(source={source})")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """No-op."""

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """No-op."""


async def handle_chat_message(
    conversation: schema.Conversation,
    user_message: schema.UserMessageCreate,
    send_chan: MemoryObjectSendStream,
) -> None:
    async with send_chan:
        chat_engine = await get_chat_engine(
            ChatCallbackHandler(send_chan), conversation
        )
        await send_chan.send(
            StreamedMessageSubProcess(
                event_id=str(uuid4()),
                has_ended=True,
                source=MessageSubProcessSourceEnum.CONSTRUCTED_QUERY_ENGINE,
            )
        )
        logger.debug("Engine received")
        templated_message = f"""
Remember - if I have asked a relevant financial question, use your tools.

{user_message.content}
        """.strip()
        streaming_chat_response: StreamingAgentChatResponse = (
            await chat_engine.astream_chat(templated_message)
        )
        response_str = ""
        response_complete = False
        async for text in streaming_chat_response.async_response_gen():
            response_str += text
            if send_chan._closed:
                logger.debug(
                    "Received streamed token after send channel closed. Ignoring."
                )
                return
            try:
                if response_str.strip():  # Only validate non-empty strings
                    validated_content = guard.validate(response_str)
                    await send_chan.send(StreamedMessage(content=validated_content.validated_output))
                    response_complete = True
                else:
                    logger.debug("Skipping validation for empty response chunk")
                    await send_chan.send(StreamedMessage(content=response_str))
            except Exception as e:
                logger.error(f"Guardrails validation failed: {str(e)}")
                await send_chan.send(
                    StreamedMessage(content="Sorry, the response was blocked due to validation issues.")
                )
                return
            # if response_complete:
            #     logger.debug("Response fully streamed; exiting generator")
            #     break
            # await send_chan.send(StreamedMessage(content=response_str))

        if response_str.strip():
            logger.debug("Response fully streamed; signaling completion")
        else:
            await send_chan.send(
                StreamedMessage(
                    content="Sorry, I either wasn't able to understand your question or I don't have an answer for it."
                )
            )
        logger.debug("Handle chat message completed")