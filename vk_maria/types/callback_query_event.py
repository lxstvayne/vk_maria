from .event import Event
from .message import CallbackQuery


class CallbackQueryEvent(Event, CallbackQuery):
    def __init__(self, vk, raw):
        super().__init__(vk, raw)

    def answer(self, event_data: dict = None):
        return self.vk.messages_send_message_event_answer(self.event_id, self.user_id, self.peer_id, event_data)
