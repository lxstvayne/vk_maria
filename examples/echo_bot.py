from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher


def main():
    """Пример простейшего бота через диспетчер"""

    vk = Vk(access_token='token')
    dp = Dispatcher(vk)

    @dp.message_handler()
    def echo(event: types.Message):
        event.answer(event.message.text)

    dp.start_polling()


if __name__ == '__main__':
    main()
