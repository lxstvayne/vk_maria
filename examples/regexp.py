from vk_maria import Vk, LongPoll


def main():
    """Проверка наличия электронной почты в сообщении"""

    vk = Vk(access_token='token')
    longpoll = LongPoll(vk)

    @longpoll.message_handler(regexp=r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    def email_check(event):
        print(f'Обнаружена почта в сообщении {event.message.text}')

    longpoll.polling()


if __name__ == '__main__':
    main()
