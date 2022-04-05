:ref: `quickstart`

Быстрый старт
--------------

Прежде всего вы должны получить `ключ доступа <https://vk.com/dev/access_token>`_ вашего сообщества.

##############################
Простейший пример
##############################

Класс ``Vk`` инкапсулирует все методы работы с токеном сообщества.

Создайте файл **echo_bot.py**. Откройте его и создайте экземпляр класса ``Vk``:

.. code-block:: python3

    from vk_maria import Vk, types
    from vk_maria.dispatcher import Dispatcher


    vk = Vk(access_token='token')

.. note:: Обязательно замените token ключом доступа вашего сообщества.

Затем создайте экземпляр класса ``Dispatcher`` передав ему в качестве аргумента ``vk``:

.. code-block:: python3

    dp = Dispatcher(vk)

После этого нам необходимо зарегистрировать обработчик событий. Обработчики событий определяют фильтры, которые должно пройти событие. Если событие проходит фильтры, вызывается декорированная функция и входящее событие передаётся в качестве аргумента.

Давайте определим обработчик событий, который будет обрабатывать все входящие сообщения от пользователя в личные сообщения сообщества и отвечать на команду Начать:

.. code-block:: python3

    @dp.message_handler(text='Начать')
    def send_welcome(event: types.Message):
        vk.messages_send(user_id=event.message.from_id, message='Добро пожаловать!')


Добавим ещё один обработчик:

.. code-block:: python3

    @dp.message_handler()
    def echo(event: types.Message):
        event.answer(event.message.text)


Как вы могли заметить, ``event.answer`` является удобным аналогом ``vk.messages_send``.

Декорированная функция может иметь произвольное имя, однако она должна принимать минимум 1 параметр (event).

.. note:: Все обработчики тестируются в том порядке, в котором они были объявлены.

Отлично, теперь у нас есть простой бот, который отвечает на сообщение Начать приветствием и повторяет остальные отправленные сообщения. Чтобы запустить бота добавьте в исходный код следующее:

.. code-block:: python3

    dp.start_polling(debug=True)

.. note:: Параметр debug отвечает за вывод в консоль всех происходящих событий

Вот и всё! Наш исходный файл теперь выглядит так:

.. code-block:: python3

    from vk_maria import Vk, types
    from vk_maria.dispatcher import Dispatcher


    vk = Vk(access_token='token')
    dp = Dispatcher(vk)


    @dp.message_handler(text='Начать')
    def send_welcome(event: types.Message):
        vk.messages_send(user_id=event.message.from_id, message='Добро пожаловать!')


    @dp.message_handler()
    def echo(event: types.Message):
        event.answer(event.message.text)


    if __name__ == '__main__':
        dp.start_polling(debug=True)


Чтобы запустить бота, просто откройте терминал, введите ``python echo_bot.py`` и протестируйте его.