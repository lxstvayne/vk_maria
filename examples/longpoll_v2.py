from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher, EventType


def main():
    """Альтернативный пример работы лонгпулла, через удобные декораторы"""

    vk = Vk(access_token='token')
    longpoll = Dispatcher(vk)

    @longpoll.event_handler(event_type=EventType.MESSAGE_NEW)
    def new_msg(event: types.Message):
        print(f'Новое сообщение для меня от {event.message.peer_id}')
        event.answer(event.message.text)

    @longpoll.event_handler(event_type=EventType.MESSAGE_REPLY)
    def reply_msg(event):
        print(f'Новое сообщение от меня для {event.peer_id}')

    @longpoll.event_handler(event_type=EventType.MESSAGE_TYPING_STATE)
    def typing_msg(event):
        print(f'{event.from_id} Печатает')

    longpoll.start_polling()


if __name__ == '__main__':
    main()
