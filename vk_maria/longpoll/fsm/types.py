import typing

from ..types import Event, EventType


class Chat:
    chat_id: int = None
    user_id: int = None

    @classmethod
    def get_chat_id(cls):
        return cls.chat_id

    @classmethod
    def get_user_id(cls):
        return cls.chat_id

    @classmethod
    def set(cls, chat_id: int, user_id: int):
        cls.chat_id = chat_id
        cls.user_id = user_id

    @staticmethod
    def resolve_address(event: Event) -> (typing.Union[int, None], typing.Union[int, None]):
        chat, user = None, None

        if event.type is EventType.MESSAGE_NEW:
            user = event.fields['message'].get('from_id')
            chat = event.fields['message'].get('peer_id')
        elif event.type is EventType.MESSAGE_EVENT:
            user = event.fields.get('user_id')
            chat = event.fields.get('peer_id')

        return chat, user
