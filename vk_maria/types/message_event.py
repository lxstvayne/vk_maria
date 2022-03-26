from .event import Event
from .message import Message
from .chat import CHAT_START_ID


class MessageEvent(Event, Message):
    def __init__(self, vk, raw):
        super().__init__(vk, raw)

        self.from_user = False
        self.from_chat = False
        self.from_group = False
        self.chat_id = None

        peer_id = self.message.peer_id if hasattr(self, 'message') else self.peer_id

        if peer_id < 0:
            self.from_group = True
        elif peer_id < CHAT_START_ID:
            self.from_user = True
        else:
            self.from_chat = True
            self.chat_id = peer_id - CHAT_START_ID

    def answer(self, message: str = None, **kwargs):
        if self.from_user:
            kwargs.update(user_id=self.message.from_id)
        elif self.from_chat:
            kwargs.update(peer_id=self.message.peer_id)
        elif self.from_group:
            kwargs.update(peer_id=self.message.from_id)

        return self.vk.messages_send(message=message, **kwargs)

    def reply(self, message: str = None, **kwargs):
        kwargs.update(reply_to=self.message.id)
        return self.answer(message=message, **kwargs)