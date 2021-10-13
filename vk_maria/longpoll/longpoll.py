from .types import EventType
from .types import Event, MessageEvent
from ..api import Vk
from .fsm import DisabledStorage, BaseStorage, FSMContext
from .fsm.types import Chat

from requests.exceptions import ReadTimeout
import re

from loguru import logger
import sys

import typing

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
    }

    __DEFAULT_EVENT_CLASS = Event

    __poll = []

    def __init__(self, vk: Vk, storage: typing.Optional[BaseStorage] = DisabledStorage()):
        self._vk = vk
        self._storage = storage
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

    # Polling

    def _add_handler(self, handler_dict):
        self.__poll.append(handler_dict)

    @staticmethod
    def _build_handler_dict(handler, **filters):
        return {
            'function': handler,
            'filters': filters
        }

    def _test_handler(self, handler_filters, event):
        handle_result = False
        event_type = handler_filters.get('event_type')
        chat_id, user_id = Chat.resolve_address(event)

        if event.type is event_type:

            if event_type is EventType.MESSAGE_NEW:
                Chat.set(chat_id=chat_id, user_id=user_id)

                commands = handler_filters.get('commands')
                frm = handler_filters.get('frm')
                regexp = handler_filters.get('regexp')
                state = handler_filters.get('state')

                type_from = getattr(event, f'from_{frm}')
                message = event.message

                if type_from:
                    if commands:
                        if message.text in commands:
                            handle_result = True
                    elif regexp:
                        if re.search(regexp, message.text, re.IGNORECASE):
                            handle_result = True
                    else:
                        handle_result = True

                if state:
                    if state == FSMContext.get_current().get_state():
                        handle_result = True
                    elif state == '*':
                        handle_result = True
                    else:
                        handle_result = False

            elif event_type in EventType:
                handle_result = True

        if handle_result:
            return True

    def event_handler(self,
                      event_type: EventType,
                      **kwargs):

        def decorator(func):
            handler_dict = self._build_handler_dict(handler=func, event_type=event_type, **kwargs)
            self._add_handler(handler_dict)

        return decorator

    def message_handler(self,
                        commands: typing.List[str] = None,
                        frm: str = 'user',
                        regexp: str = None,
                        state=None):
        return self.event_handler(event_type=EventType.MESSAGE_NEW,
                                  commands=commands,
                                  frm=frm,
                                  regexp=regexp,
                                  state=state)

    def polling(self, debug=False):
        for event in self.listen():

            if debug:
                logger.info(event)

            for handler in self.__poll:
                if self._test_handler(handler['filters'], event):
                    handler = handler['function']
                    if handler.__code__.co_argcount == 2:
                        handler(event, FSMContext.get_current())
                    else:
                        handler(event)
                    break
