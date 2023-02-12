import sys
import typing

from loguru import logger

from ..longpoll import LongPoll
from .filters.handler import HandlerManager
from .fsm import DisabledStorage, BaseStorage, FSMContext
from ..types import EventType, Chat


logger.remove()
logger.add(sys.stdout,
           level='INFO',
           colorize=True,
           format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> <b><red>| {level} |</red> {message}</b>")


class Dispatcher:
    def __init__(self, vk, storage: typing.Optional[BaseStorage] = DisabledStorage()):
        self._vk = vk
        self._longpoll = LongPoll(vk)
        self._storage = storage
        self._handler_manager = HandlerManager()
        FSMContext(storage)

    def register_event_handler(self,
                               function: callable,
                               event_type: EventType,
                               *filters,
                               **bound_filters):
        bound_filters = {k: v for k, v in bound_filters.items() if v is not None}
        self._handler_manager.register_handler(function, event_type=event_type, *filters, **bound_filters)

    def register_message_handler(self,
                                 function: callable,
                                 *filters,
                                 commands: typing.List[str] = None,
                                 frm: str = 'user',
                                 regexp: str = None,
                                 state=None,
                                 **kwargs):
        self.register_event_handler(function,
                                    EventType.MESSAGE_NEW,
                                    *filters,
                                    commands=commands,
                                    frm=frm,
                                    regexp=regexp,
                                    state=state,
                                    **kwargs)

    def register_callback_handler(self,
                                  function: callable,
                                  *filters,
                                  state=None,
                                  **bound_filters):
        self.register_event_handler(function,
                                    EventType.MESSAGE_EVENT,
                                    *filters,
                                    state=state,
                                    **bound_filters)

    def event_handler(self,
                      event_type: EventType,
                      *filters,
                      **bound_filters):
        def wrapper(callback):
            self.register_event_handler(callback, event_type, *filters, **bound_filters)
            return callback

        return wrapper

    def message_handler(self,
                        *filters,
                        commands: typing.List[str] = None,
                        frm: str = 'user',
                        regexp: str = None,
                        state=None,
                        **bound_filters):
        return self.event_handler(EventType.MESSAGE_NEW,
                                  *filters,
                                  commands=commands,
                                  frm=frm,
                                  regexp=regexp,
                                  state=state,
                                  **bound_filters)

    def callback_handler(self,
                         *filters,
                         state=None,
                         payload=None,
                         **bound_filters):
        return self.event_handler(EventType.MESSAGE_EVENT,
                                  *filters,
                                  state=state,
                                  payload=payload,
                                  **bound_filters)

    @staticmethod
    def _update_chat_context(event):
        if event.type in (
            EventType.MESSAGE_NEW,
            EventType.MESSAGE_EVENT,
        ):
            chat_id, user_id = Chat.resolve_address(event)
            Chat.set(chat_id, user_id)

    def start_polling(self, debug=False, on_startup=None, on_shutdown=None):
        if on_startup:
            on_startup()
        try:
            for event in self._longpoll.listen():

                if debug:
                    logger.info(event)

                self._update_chat_context(event)

                for handler in self._handler_manager.handlers:
                    if handler.test_handler(event):
                        handler(event)
                        break
        except Exception as e:
            if debug:
                logger.exception(e)
        finally:
            if on_shutdown:
                on_shutdown()
                return

            self._storage.close()
