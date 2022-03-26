from vk_maria import Vk
from vk_maria.dispatcher import Dispatcher


def main():
    """Проверка наличия электронной почты в сообщении"""

    vk = Vk(access_token='token')
    dp = Dispatcher(vk)

    @dp.message_handler(regexp=r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    def email_check(event):
        print(f'Обнаружена почта в сообщении {event.message.text}')

    dp.start_polling()


if __name__ == '__main__':
    main()
