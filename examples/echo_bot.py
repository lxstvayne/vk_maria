from vk_maria import Vk, types
from vk_maria.longpoll import LongPoll


def main():
    """Пример простейшего бота через декоратор лонгпулла"""

    vk = Vk(access_token='token')
    longpoll = LongPoll(vk)

    @longpoll.message_handler()
    def echo(event: types.Message):
        event.answer(event.message.text)

    longpoll.polling()


if __name__ == '__main__':
    main()
