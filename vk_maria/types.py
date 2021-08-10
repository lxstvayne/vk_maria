from typing import Union, Dict, List
from pydotdict import DotDict


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


class Message:
    message: MessageInfo
    from_user: bool
    from_chat: bool
    from_group: bool
    chat_id: Union[int, None]
    peer_id: int = None

    def answer(self, domain: str = None,
               chat_id: int = None, message: str = None, lat: float = None, long: float = None, attachment=None,
               reply_to: int = None, forward_messages: List[int] = None, forward=None, sticker_id: int = None,
               keyboard=None, template: Dict = None, payload=None, content_source: Dict = None,
               dont_parse_links: int = None, disable_mentions: int = None, intent: str = 'default',
               subscribe_id: int = None): pass
    def reply(self): pass