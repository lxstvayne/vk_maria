from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.types import Button, KeyboardModel, Color


class MyKeyboard(KeyboardModel):
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
    dp = Dispatcher(vk)

    @dp.message_handler()
    def echo(event: types.Message):
        event.answer('Смотри какая есть клавиатура!', keyboard=MyKeyboard)

    dp.start_polling()


if __name__ == '__main__':
    main()
