from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher


def main():
    """Пример простейшего бота через декоратор лонгпулла"""

    vk = Vk(access_token='token')
    longpoll = Dispatcher(vk)

    @longpoll.message_handler()
    def echo(event: types.Message):
        event.answer(event.message.text)

    longpoll.start_polling()


if __name__ == '__main__':
    main()
