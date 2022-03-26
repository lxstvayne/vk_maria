from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.dispatcher.filters import AbstractFilter, BoundFilter


ADMIN_ID = 1234567890


class IsAdmin(AbstractFilter):
    def check(self, event: types.Message):
        return event.message.peer_id == ADMIN_ID


class FromIdFilter(BoundFilter):
    key = 'from_id'  # По ключу мы сможем ставить фильтр в message_event

    def __init__(self, id_: int):
        self.id = id_

    def check(self, event: types.Message):
        return self.id == event.message.from_id


def main():
    """Пример использования кастомных фильтров"""

    vk = Vk(access_token='token')
    dp = Dispatcher(vk)

    @dp.message_handler(IsAdmin)
    def echo(event: types.Message):
        event.answer('Привет, Администратор!')

    @dp.message_handler(from_id=1234567890)
    def echo(event: types.Message):
        event.answer('Привет, Администратор!')

    dp.start_polling(debug=True)


if __name__ == '__main__':
    main()
