import sys
import typing

from loguru import logger
from requests.exceptions import ReadTimeout

from .filters.handler import HandlerManager
from .fsm import DisabledStorage, BaseStorage, FSMContext
from .fsm.types import Chat
from .types import Event, MessageEvent, CallbackQueryEvent, EventType
from ..api import Vk

logger.remove()
logger.add(sys.stdout,
           level='INFO',
           colorize=True,
           format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> <b><red>| {level} |</red> {message}</b>"
           )


class LongPoll:
    __CLASS_BY_EVENT_TYPE = {
        EventType.MESSAGE_NEW.value: MessageEvent,
        EventType.MESSAGE_REPLY.value: MessageEvent,
        EventType.MESSAGE_EDIT.value: MessageEvent,
        EventType.MESSAGE_EVENT.value: CallbackQueryEvent
    }

    __DEFAULT_EVENT_CLASS = Event

    __poll = []

    def __init__(self, vk: Vk, storage: typing.Optional[BaseStorage] = DisabledStorage()):
        self._vk = vk
        self._storage = storage
        self._handler_manager = HandlerManager()
        FSMContext(storage)

        self._wait = 25
        self._key, self._server, self._ts = self._vk.groups_get_longpoll_server().values()

    def _update_longpoll(self, update_ts=True):
        response = self._vk.groups_get_longpoll_server()
        self._server = response['server']
        self._key = response['key']
        if update_ts:
            self._ts = response['ts']

    def _parse_event(self, raw_event):
        event_class = self.__CLASS_BY_EVENT_TYPE.get(
            raw_event['type'],
            self.__DEFAULT_EVENT_CLASS
        )
        return event_class(self._vk, raw_event)

    def _check(self):
        response = self._vk.method(server=self._server, key=self._key, ts=self._ts, wait=self._wait, act='a_check')

        if 'failed' not in response:
            self._ts = response['ts']
            return [self._parse_event(raw_event) for raw_event in response['updates']]

        elif response['failed'] == 1:
            self._ts = response['ts']

        elif response['failed'] == 2:
            self._update_longpoll(update_ts=False)

        elif response['failed'] == 3:
            self._update_longpoll()

        return []

    def listen(self):
        while True:
            try:
                for event in self._check():
                    yield event
            except ReadTimeout:
                pass

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
                         **bound_filters):
        return self.event_handler(EventType.MESSAGE_EVENT,
                                  *filters,
                                  state=state,
                                  **bound_filters)

    @staticmethod
    def _update_chat_context(event):
        chat_id, user_id = Chat.resolve_address(event)
        if event.type == EventType.MESSAGE_NEW:
            Chat.set(chat_id, user_id)

    def polling(self, debug=False):
        for event in self.listen():

            if debug:
                logger.info(event)

            self._update_chat_context(event)

            for handler in self._handler_manager.handlers:
                if handler.test_handler(event):
                    handler(event)
                    break
