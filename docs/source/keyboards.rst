:ref: `keyboards`

Клавиатуры
------------

Клавиатуры можно создавать двумя способами

#######################
KeyboardModel
#######################

С помощью определения класса

.. code-block:: python3

    from vk_maria.types import KeyboardModel, Button, Color

    class TestKeyboard(KeyboardModel):

        one_time = True

        row1 = [
            Button.Text(Color.PRIMARY, 'Кнопка 1'),
            Button.Text(Color.PRIMARY, 'Кнопка 2')
        ]
        row2 = [
            Button.Text(Color.PRIMARY, 'Кнопка 3'),
            Button.Text(Color.PRIMARY, 'Кнопка 4')
        ]

#######################
KeyboardMarkup
#######################

С помощью генерации через код

.. code-block:: python3

    from vk_maria.types import KeyboardMarkup, Button, Color

    markup = KeyboardMarkup(one_time=True)
    markup.add_button(Button.Text(Color.PRIMARY, 'Кнопка 1'))
    markup.add_button(Button.Text(Color.PRIMARY, 'Кнопка 2'))
    markup.add_row()
    markup.add_button(Button.Text(Color.PRIMARY, 'Кнопка 3'))
    markup.add_button(Button.Text(Color.PRIMARY, 'Кнопка 4'))