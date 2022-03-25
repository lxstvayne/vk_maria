import copy
import typing

from vk_maria.longpoll.fsm.storage.core import BaseStorage


class MemoryStorage(BaseStorage):

    def close(self):
        self.data.clear()

    def __init__(self):
        self.data = {}

    def resolve_address(self, chat, user):
        chat_id, user_id = map(int, self.check_address(chat=chat, user=user))

        if chat_id not in self.data:
            self.data[chat_id] = {}
        if user_id not in self.data[chat_id]:
            self.data[chat_id][user_id] = {'state': None, 'data': {}}

        return chat_id, user_id

    def get_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  default: typing.Optional[str] = None) -> typing.Optional[str]:
        chat, user = self.resolve_address(chat=chat, user=user)
        return self.data[chat][user].get('state', default)

    def get_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        chat, user = self.resolve_address(chat=chat, user=user)
        return copy.deepcopy(self.data[chat][user]['data'])

    def set_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        chat, user = self.resolve_address(chat=chat, user=user)
        self.data[chat][user]['state'] = state

    def set_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 data: typing.Dict = None):
        if data is None:
            data = {}
        chat, user = self.resolve_address(chat=chat, user=user)
        self.data[chat][user]['data'] = data

    def update_data(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None,
                    data: typing.Dict = None,
                    **kwargs):
        if data is None:
            data = {}
        chat, user = self.resolve_address(chat=chat, user=user)
        self.data[chat][user]['data'].update(data, **kwargs)

    def reset_state(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None,
                    with_data: typing.Optional[bool] = True):
        self.set_state(chat=chat, user=user, state=None)
        if with_data:
            self.set_data(chat=chat, user=user, data={})
        self._cleanup(chat, user)

    def _cleanup(self, chat, user):
        chat, user = self.resolve_address(chat=chat, user=user)
        if self.data[chat][user] == {'state': None, 'data': {}}:
            del self.data[chat][user]
        if not self.data[chat]:
            del self.data[chat]