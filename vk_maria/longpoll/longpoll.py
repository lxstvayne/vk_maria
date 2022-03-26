from requests import ReadTimeout

from ..types import Event, MessageEvent, CallbackQueryEvent, EventType


class LongPoll:
    __CLASS_BY_EVENT_TYPE = {
        EventType.MESSAGE_NEW.value: MessageEvent,
        EventType.MESSAGE_REPLY.value: MessageEvent,
        EventType.MESSAGE_EDIT.value: MessageEvent,
        EventType.MESSAGE_EVENT.value: CallbackQueryEvent
    }

    __DEFAULT_EVENT_CLASS = Event

    def __init__(self, vk):
        self._vk = vk
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
