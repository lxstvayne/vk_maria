from ..longpoll import EventType
import typing
from pydotdict import DotDict


class BaseEvent:
    type: EventType


class MessageInfo(DotDict):
    date: int
    from_id: int
    id: int
    out: int
    peer_id: int
    text: str
    conversation_message_id: int
    fwd_messages: list
    important: bool
    random_id: int
    attachments: list
    is_hidden: bool


class Message(BaseEvent):
    message: MessageInfo
    from_user: bool
    from_chat: bool
    from_group: bool
    chat_id: typing.Union[int, None]
    peer_id: int

    def answer(self, message: str = None, domain: str = None, lat: float = None,
               long: float = None, attachment=None, reply_to: int = None, forward_messages: typing.List[int] = None,
               forward=None, sticker_id: int = None, keyboard=None, template: typing.Dict = None, payload=None,
               content_source: typing.Dict = None, dont_parse_links: int = None, disable_mentions: int = None,
               intent: str = 'default', subscribe_id: int = None): pass

    def reply(self, message: str = None, domain: str = None, lat: float = None,
               long: float = None, attachment=None, reply_to: int = None, forward_messages: typing.List[int] = None,
               forward=None, sticker_id: int = None, keyboard=None, template: typing.Dict = None, payload=None,
               content_source: typing.Dict = None, dont_parse_links: int = None, disable_mentions: int = None,
               intent: str = 'default', subscribe_id: int = None):
        '''
        Не работает в беседах из-за ограниченного апи
        '''
        pass