from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.types import EventType


def main():
    """Обработка событий через диспетчер"""

    vk = Vk(access_token='token')
    dp = Dispatcher(vk)

    @dp.event_handler(event_type=EventType.MESSAGE_NEW)
    def new_msg(event: types.Message):
        print(f'Новое сообщение для меня от {event.message.peer_id}')
        event.answer(event.message.text)

    @dp.event_handler(event_type=EventType.MESSAGE_REPLY)
    def reply_msg(event):
        print(f'Новое сообщение от меня для {event.peer_id}')

    @dp.event_handler(event_type=EventType.MESSAGE_TYPING_STATE)
    def typing_msg(event):
        print(f'{event.from_id} Печатает')

    dp.start_polling()


if __name__ == '__main__':
    main()
