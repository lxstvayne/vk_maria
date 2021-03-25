from vk_maria import Vk, LongPoll


def main():
    """Пример простейшего бота через декоратор лонгпулла"""

    vk = Vk(access_token='token')
    longpoll = LongPoll(vk)

    @longpoll.event_handler()
    def echo(event):
        vk.messages_send(user_id=event.message.from_id, message=event.message.text)

    longpoll.polling()


if __name__ == '__main__':
    main()
