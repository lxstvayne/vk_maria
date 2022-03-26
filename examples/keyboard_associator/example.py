from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.keyboard import KeyboardModel, Button, Color, KeyboardAssociator
import random


class MyKeyboard(KeyboardModel):
    inline = True
    # Очень важно перечислять строки с ключевого слова row и по порядку.
    row1 = [
        Button.TextButton(Color.PRIMARY, 'Нажми на меня'),
        Button.TextButton(Color.NEGATIVE, 'Не нажимай')
    ]
    row2 = [
        Button.OpenLinkButton('https://vk.com/dev/manuals', 'Открыть документацию')
    ]


def main():
    """Пример использования классов клавиатур"""

    vk = Vk(access_token='token')
    longpoll = Dispatcher(vk)
    keyboard = KeyboardAssociator(models=__name__, folder='json_keyboards')

    @longpoll.message_handler()
    def echo(event: types.Message):
        kb = random.choice((keyboard.MyKeyboard, keyboard.keyboard1, keyboard['keyboard2']))
        event.answer('Смотри какая есть клавиатура!', keyboard=kb)

    longpoll.start_polling()


if __name__ == '__main__':
    main()
