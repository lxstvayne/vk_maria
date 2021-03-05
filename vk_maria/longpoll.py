from .api import Vk

from requests.exceptions import ReadTimeout
from enum import Enum
from pydotdict import DotDict
import re

from loguru import logger
import sys
from typing import Union, List

logger.remove()
logger.add(sys.stdout,
           level='INFO',
           colorize=True,
           format="<green>{time:DD.MM.YYYY HH:mm:ss}</green> <b><red>| {level} |</red> {message}</b>"
)

CHAT_START_ID = int(2E9)

class EventType(Enum):
    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGE_EVENT = 'message_event'

    MESSAGE_TYPING_STATE = 'message_typing_state'

    MESSAGE_ALLOW = 'message_allow'

    MESSAGE_DENY = 'message_deny'

    PHOTO_NEW = 'photo_new'

    PHOTO_COMMENT_NEW = 'photo_comment_new'
    PHOTO_COMMENT_EDIT = 'photo_comment_edit'
    PHOTO_COMMENT_RESTORE = 'photo_comment_restore'

    PHOTO_COMMENT_DELETE = 'photo_comment_delete'

    AUDIO_NEW = 'audio_new'

    VIDEO_NEW = 'video_new'

    VIDEO_COMMENT_NEW = 'video_comment_new'
    VIDEO_COMMENT_EDIT = 'video_comment_edit'
    VIDEO_COMMENT_RESTORE = 'video_comment_restore'

    VIDEO_COMMENT_DELETE = 'video_comment_delete'

    WALL_POST_NEW = 'wall_post_new'
    WALL_REPOST = 'wall_repost'

    WALL_REPLY_NEW = 'wall_reply_new'
    WALL_REPLY_EDIT = 'wall_reply_edit'
    WALL_REPLY_RESTORE = 'wall_reply_restore'

    WALL_REPLY_DELETE = 'wall_reply_delete'

    BOARD_POST_NEW = 'board_post_new'
    BOARD_POST_EDIT = 'board_post_edit'
    BOARD_POST_RESTORE = 'board_post_restore'

    BOARD_POST_DELETE = 'board_post_delete'

    MARKET_COMMENT_NEW = 'market_comment_new'
    MARKET_COMMENT_EDIT = 'market_comment_edit'
    MARKET_COMMENT_RESTORE = 'market_comment_restore'

    MARKET_COMMENT_DELETE = 'market_comment_delete'

    GROUP_LEAVE = 'group_leave'

    GROUP_JOIN = 'group_join'

    USER_BLOCK = 'user_block'

    USER_UNBLOCK = 'user_unblock'

    POLL_VOTE_NEW = 'poll_vote_new'

    GROUP_OFFICERS_EDIT = 'group_officers_edit'

    GROUP_CHANGE_SETTINGS = 'group_change_settings'

    GROUP_CHANGE_PHOTO = 'group_change_photo'

    VKPAY_TRANSACTION = 'vkpay_transaction'


class Event:

    def __init__(self, raw):

        try:
            self.type = EventType(raw['type'])
        except ValueError:
            self.type = raw['type']

        for k, v in raw['object'].items():
            self.__dict__.update({k: DotDict(v) if isinstance(v, dict) else v})

        self.group_id = raw['group_id']

    def __repr__(self):
        return f'<{self.__class__.__name__}({", ".join(f"{k}={v}" for k, v in self.__dict__.items())})>'


class Message(DotDict):
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


class MessageEvent(Event):

    message: Message
    from_user: bool
    from_chat: bool
    from_group: bool
    chat_id: Union[int, None]
    peer_id: int = None

    def __init__(self, raw):
        super().__init__(raw)

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

class LongPoll:

    CLASS_BY_EVENT_TYPE = {
        EventType.MESSAGE_NEW.value: MessageEvent,
        EventType.MESSAGE_REPLY.value: MessageEvent,
        EventType.MESSAGE_EDIT.value: MessageEvent,
    }

    DEFAULT_EVENT_CLASS = Event

    def __init__(self, vk: Vk):
        self.vk = vk
        self.wait = 25
        self.key, self.server, self.ts = self.vk.groups_get_longpoll_server().values()

    def _update_longpoll(self, update_ts=True):
        response = self.vk.groups_get_longpoll_server()
        self.server = response['server']
        self.key = response['key']
        if update_ts:
            self.ts = response['ts']

    def _parse_event(self, raw_event):
        event_class = self.CLASS_BY_EVENT_TYPE.get(
            raw_event['type'],
            self.DEFAULT_EVENT_CLASS
        )
        return event_class(raw_event)

    def _check(self):
        response = self.vk.method(server=self.server, key=self.key, ts=self.ts, wait=self.wait, act='a_check')

        if 'failed' not in response:
            self.ts = response['ts']
            return [self._parse_event(raw_event) for raw_event in response['updates']]

        elif response['failed'] == 1:
            self.ts = response['ts']

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
        self.poll.append(handler_dict)

    @staticmethod
    def _build_handler_dict(handler, **filters):
        return {
            'function': handler,
            'filters': filters
        }

    @staticmethod
    def _test_handler(handler_filters, event):

        event_type = handler_filters.get('event_type')

        if event.type is event_type:

            if event_type is EventType.MESSAGE_NEW:
                commands = handler_filters.get('commands')
                frm = handler_filters.get('frm')
                regexp = handler_filters.get('regexp')

                type_from = getattr(event, f'from_{frm}')
                message = event.message

                if type_from:
                    if commands:
                        if message.text in commands:
                            return True
                    elif regexp:
                        if re.search(regexp, message.text, re.IGNORECASE):
                            return True
                    else:
                        return True

            elif event_type in EventType:
                return True

    poll = []

    def message_handler(self,
                        commands: List = None,
                        frm: str = 'user',
                        event_type: EventType = EventType.MESSAGE_NEW,
                        regexp: str = None
                        ):

        def decorator(func):

            filters = dict(commands=commands, frm=frm, event_type=event_type, regexp=regexp)

            handler_dict = self._build_handler_dict(
                handler=func,
                **filters
            )

            self._add_handler(handler_dict)

        return decorator

    def polling(self, debug=False):
        for event in self.listen():

            if debug:
                logger.info(event)

            for message_handler in self.poll:
                if self._test_handler(message_handler['filters'], event):
                    message_handler['function'](event)
                    break
