import copy
import typing
from abc import ABC, abstractmethod

from loguru import logger

from .types import Chat
from ..mixins import ContextInstanceMixin


class BaseStorage(ABC):

    @abstractmethod
    def close(self):
        pass

    @classmethod
    def check_address(cls, *,
                      chat: typing.Union[str, int, None] = None,
                      user: typing.Union[str, int, None] = None
                      ) -> (typing.Union[str, int], typing.Union[str, int]):

        if chat is None and user is None:
            raise ValueError('`user` or `chat` parameter is required but no one is provided!')

        if user is None:
            user = chat

        elif chat is None:
            chat = user

        return chat, user

    @abstractmethod
    def get_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  default: typing.Optional[str] = None) -> typing.Optional[str]:
        pass

    @abstractmethod
    def get_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        pass

    @abstractmethod
    def set_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        pass

    @abstractmethod
    def set_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 data: typing.Dict = None):
        pass

    @abstractmethod
    def update_data(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None,
                    data: typing.Dict = None,
                    **kwargs):
        pass

    def reset_data(self, *,
                   chat: typing.Union[str, int, None] = None,
                   user: typing.Union[str, int, None] = None):
        self.set_data(chat=chat, user=user, data={})

    def reset_state(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None,
                    with_data: typing.Optional[bool] = True):
        chat, user = self.check_address(chat=chat, user=user)
        self.set_state(chat=chat, user=user, state=None)
        if with_data:
            self.set_data(chat=chat, user=user, data={})

    def finish(self, *,
               chat: typing.Union[str, int, None] = None,
               user: typing.Union[str, int, None] = None):
        self.reset_state(chat=chat, user=user, with_data=True)


class FSMContext(ContextInstanceMixin):
    def __init__(self, storage: BaseStorage):
        self.storage: BaseStorage = storage

    def get_state(self, default: typing.Optional[str] = None) -> typing.Optional[str]:
        return self.storage.get_state(chat=Chat.get_chat_id(), user=Chat.get_user_id(), default=default)

    def get_data(self, default: typing.Optional[str] = None) -> typing.Dict:
        return self.storage.get_data(chat=Chat.get_chat_id(), user=Chat.get_user_id(), default=default)

    def update_data(self, data: typing.Dict = None, **kwargs):
        self.storage.update_data(chat=Chat.get_chat_id(), user=Chat.get_user_id(), data=data, **kwargs)

    def set_state(self, state: typing.Optional[typing.AnyStr] = None):
        self.storage.set_state(chat=Chat.get_chat_id(), user=Chat.get_user_id(), state=state)

    def set_data(self, data: typing.Dict = None):
        self.storage.set_data(chat=Chat.get_chat_id(), user=Chat.get_user_id(), data=data)

    def reset_state(self, with_data: typing.Optional[bool] = True):
        self.storage.reset_state(chat=Chat.get_chat_id(), user=Chat.get_user_id(), with_data=with_data)

    def reset_data(self):
        self.storage.reset_data(chat=Chat.get_chat_id(), user=Chat.get_user_id(), )

    def finish(self):
        self.storage.finish(chat=Chat.get_chat_id(), user=Chat.get_user_id(), )


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


class DisabledStorage(BaseStorage):

    def close(self):
        pass

    def get_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  default: typing.Optional[str] = None) -> typing.Optional[str]:
        return None

    def get_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        self._warning()
        return {}

    def update_data(self, *,
                    chat: typing.Union[str, int, None] = None,
                    user: typing.Union[str, int, None] = None,
                    data: typing.Dict = None,
                    **kwargs):
        self._warning()

    def set_state(self, *,
                  chat: typing.Union[str, int, None] = None,
                  user: typing.Union[str, int, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        self._warning()

    def set_data(self, *,
                 chat: typing.Union[str, int, None] = None,
                 user: typing.Union[str, int, None] = None,
                 data: typing.Dict = None):
        self._warning()

    def _warning(self):
        logger.warning('Вы не указали хранилище состояний')
