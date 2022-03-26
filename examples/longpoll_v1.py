from vk_maria import Vk
from vk_maria.dispatcher import Dispatcher, EventType


def main():
    """Пример работы лонгпулла через цикл"""

    vk = Vk(access_token='token')

    for event in Dispatcher(vk).listen():

        if event.type is EventType.MESSAGE_NEW:
            print(f'Новое сообщение для меня от {event.message.peer_id}')
            vk.messages_send(user_id=event.message.from_id, message=event.message.text)

        if event.type is EventType.MESSAGE_REPLY:
            print(f'Новое сообщение от меня для {event.peer_id}')

        if event.type is EventType.MESSAGE_TYPING_STATE:
            print(f'{event.from_id} Печатает')


if __name__ == '__main__':
    main()
