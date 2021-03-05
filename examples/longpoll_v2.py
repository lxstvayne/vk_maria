from vk_maria import Vk, LongPoll, EventType


def main():
    """Альтернативный пример работы лонгпулла, через удобные декораторы"""

    vk = Vk(access_token='token')
    longpoll = LongPoll(vk)

    @longpoll.message_handler(event_type=EventType.MESSAGE_NEW)
    def new_msg(event):
        print(f'Новое сообщение для меня от {event.message.peer_id}')
        vk.messages_send(user_id=event.message.from_id, message=event.message.text)

    @longpoll.message_handler(event_type=EventType.MESSAGE_REPLY)
    def reply_msg(event):
        print(f'Новое сообщение от меня для {event.peer_id}')

    @longpoll.message_handler(event_type=EventType.MESSAGE_TYPING_STATE)
    def typing_msg(event):
        print(f'{event.from_id} Печатает')

    longpoll.polling()


if __name__ == '__main__':
    main()
