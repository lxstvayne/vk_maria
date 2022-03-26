from vk_maria import Vk
from vk_maria.dispatcher import Dispatcher


def main():
    """Проверка наличия электронной почты в сообщении"""

    vk = Vk(access_token='token')
    longpoll = Dispatcher(vk)

    @longpoll.message_handler(regexp=r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    def email_check(event):
        print(f'Обнаружена почта в сообщении {event.message.text}')

    longpoll.start_polling()


if __name__ == '__main__':
    main()
