from enum import Enum

from pydotdict import DotDict

from ..types import Message, CallbackQuery

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
    def __init__(self, vk, raw):

        self.vk = vk
        self.fields = {}

        try:
            self.type = EventType(raw['type'])
        except ValueError:
            self.type = raw['type']

        self.fields.update({'type': self.type})

        for k, v in raw['object'].items():
            self.fields.update({k: DotDict(v) if isinstance(v, dict) else v})

        self.__dict__.update(self.fields)

        self.group_id = raw['group_id']

    def __repr__(self):
        return f'<{self.__class__.__name__}({", ".join(f"{k}={v}" for k, v in self.fields.items())})>'


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


class CallbackQueryEvent(Event, CallbackQuery):
    def __init__(self, vk, raw):
        super().__init__(vk, raw)

    def answer(self, event_data: dict = None):
        return self.vk.messages_send_message_event_answer(self.event_id, self.user_id, self.peer_id, event_data)
