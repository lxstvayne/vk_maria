from vk_maria import Vk, types
from vk_maria.longpoll import LongPoll
from vk_maria.keyboard import Model, Button, Color, KeyboardAssociator
import random


class MyKeyboard(Model):
    inline = True
    # Очень важно перечислять строки с ключевого слова row и по порядку.
    row1 = [
        Button.Text(Color.PRIMARY, 'Нажми на меня'),
        Button.Text(Color.NEGATIVE, 'Не нажимай')
    ]
    row2 = [
        Button.OpenLink('https://vk.com/dev/manuals', 'Открыть документацию')
    ]


def main():
    """Пример использования классов клавиатур"""

    vk = Vk(access_token='token')
    longpoll = LongPoll(vk)
    keyboard = KeyboardAssociator(module=__name__, folder='json_keyboards')

    @longpoll.message_handler()
    def echo(event: types.Message):
        kb = random.choice((keyboard.MyKeyboard, keyboard.keyboard1, keyboard['keyboard2']))
        event.answer('Смотри какая есть клавиатура!', keyboard=kb)

    longpoll.polling()


if __name__ == '__main__':
    main()
