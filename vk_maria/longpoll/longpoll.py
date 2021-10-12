from .types import EventType
from .types import Event, MessageEvent
from ..api import Vk
from ..longpoll.mixins import ContextInstanceMixin
from .storage import DisabledStorage
from .storage import BaseStorage, FSMContext
from ..longpoll.types import Chat

from requests.exceptions import ReadTimeout
import re
from functools import partial

from loguru import logger
import sys

import typing

logger.remove()
logger.add(sys.stdout,
           level='INFO',
           colorize=True,
           format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> <b><red>| {level} |</red> {message}</b>"
           )


class FiltersFactory:
    def __init__(self, lp):
        self.lp = lp

    def bind(self, handler_filters: dict):
        filters_ = {
            'event_type': lambda event_type, event: event.type is event_type,
            'frm': lambda frm, event: getattr(event, f'from_{frm}'),
            'commands': lambda commands, event: event.message.text in commands,
            'regexp': lambda regexp, event: re.search(regexp, event.message.text, re.IGNORECASE),
            'state': lambda state, event: (hasattr(LongPoll, '_context')
                                           and state == self.lp.current_context().get_state()
                                           ) or state == '*'
        }

        filters = {}

        for filter_name, filter_value in handler_filters.items():
            if filter_value:
                # if not filters_[filter_name](filter_value, event):
                #     return False
                filters[filter_name] = filters_[filter_name]

        return filters


class HandlerObject:
    def __init__(self,
                 func,
                 **filters):
        self.function = func
        self.filters = filters

    def test_handler(self, handle_value, event):
        for filter_name, filter_value in self.filters.items():
            if filter_name != handle_value:
                pass
            if not filter_value(handle_value, event):
                return False

        return True


class LongPoll(ContextInstanceMixin):
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

    def current_context(self):
        return self._context

    def _update_state(self, *,
                      chat: typing.Union[int, None],
                      user: typing.Union[int, None]):
        self._context = FSMContext(storage=self._storage, chat=chat, user=user)

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
        chat, user = Chat.resolve_address(event)

        # factory = FiltersFactory(self)
        # if factory.test(handler_filters, event):
        #     handle_result = True

        if event.type is event_type:

            if event_type is EventType.MESSAGE_NEW:
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
                    if hasattr(self, '_context') and state == self._context.get_state():
                        handle_result = True
                    elif state == '*':
                        handle_result = True
                    else:
                        handle_result = False

            elif event_type in EventType:
                handle_result = True

        if handle_result:
            self._update_state(chat=chat, user=user)
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
                        handler(event, self._context)
                    else:
                        handler(event)
                    break
