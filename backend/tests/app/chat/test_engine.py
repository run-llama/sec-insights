from typing import List, Tuple, Optional
from uuid import UUID, uuid4
from datetime import datetime
from llama_index.llms import ChatMessage
from app.schema import Message
from app.models.db import MessageStatusEnum, MessageRoleEnum
from app.chat.engine import get_chat_history


class MockMessage(Message):
    conversation_id: UUID = uuid4()
    sub_processes: list = []


def chat_tuples_to_chat_messages(
    chat_tuples: List[Tuple[Optional[str], Optional[str]]]
) -> ChatMessage:
    """
    Convert a list of chat tuples to a list of chat messages.
    Really only wrote this helper method to make it easier to define what
    the expected chat history should be in the tests.
    """
    chat_messages = []
    for user_message, assistant_message in chat_tuples:
        if user_message:
            chat_messages.append(
                ChatMessage(
                    content=user_message,
                    role=MessageRoleEnum.user,
                )
            )
        if assistant_message:
            chat_messages.append(
                ChatMessage(
                    content=assistant_message,
                    role=MessageRoleEnum.assistant,
                )
            )
    return chat_messages


class TestGetChatHistory:
    """
    Test the get_chat_history function.
    """

    def test_get_chat_history_happy_path(self):
        messages = [
            MockMessage(
                content="Hello",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
            MockMessage(
                content="How are you?",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 2),
            ),
            MockMessage(
                content="Good, thank you",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 3),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages(
            [("Hello", "Hi"), ("How are you?", "Good, thank you")]
        )
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_multiple_consecutive_messages_from_same_role(self):
        messages = [
            MockMessage(
                content="Hello",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="How are you?",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 2),
            ),
            MockMessage(
                content="Good, thank you",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 3),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages(
            [
                ("Hello", None),
                ("How are you?", "Hi"),
                (None, "Good, thank you"),
            ]
        )
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_empty_input(self):
        messages = []
        expected_result = []
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_error_status(self):
        messages = [
            MockMessage(
                content="Hello",
                status=MessageStatusEnum.ERROR,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages(
            [
                (None, "Hi"),
            ]
        )
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_error_status_assistant_message(self):
        messages = [
            MockMessage(
                content="Hello",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
            MockMessage(
                content="How are you?",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 2),
            ),
            MockMessage(
                content="Good, thank you",
                status=MessageStatusEnum.ERROR,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 3),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages(
            [("Hello", "Hi"), ("How are you?", None)]
        )
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_strip_content(self):
        messages = [
            MockMessage(
                content="    ",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages([(None, "Hi")])
        assert get_chat_history(messages) == expected_result

    def test_get_chat_history_unpaired_user_message(self):
        messages = [
            MockMessage(
                content="Hello",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 0),
            ),
            MockMessage(
                content="Hi",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.assistant,
                created_at=datetime(2023, 1, 1, 12, 1),
            ),
            MockMessage(
                content="How are you?",
                status=MessageStatusEnum.SUCCESS,
                role=MessageRoleEnum.user,
                created_at=datetime(2023, 1, 1, 12, 2),
            ),
        ]
        expected_result = chat_tuples_to_chat_messages(
            [("Hello", "Hi"), ("How are you?", None)]
        )
        assert get_chat_history(messages) == expected_result
