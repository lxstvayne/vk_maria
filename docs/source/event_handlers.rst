:ref: `event_handling`

Обработчики событий
---------------------

Обработчик событий это функция с декоратором ``event_handler()``. Он определяет фильтры для обрабатываемых событий.

.. code-block:: python3

    @dp.event_handler(event_type, *filters, **bound_filters)
    def handler(event):
        ...

Для удобной работы с сообщениями, существует декоратор ``message_handler(*filters, **bound_filters)``, в который по стандарту передаётся ``types.EventType.MESSAGE_NEW``.

Связанные фильтры устанавливаются следующим образом: ``name=argument``

.. csv-table:: Доступные связанные фильтры
    :header: "Название", "Аргументы", "Условие"
    :widths: 15, 20, 40

    "event_type", "types.EventType", "**True**, если типы событий совпадают."
    "text", "Строка", "**True**, если текст сообщения совпадает с аргументом **text**"
    "regexp", "Регулярное выражение или подстрока", "**True**, если подстрока находится в сообщении или строка проходит проверку на наличие шаблона регулярного выражения (Подробнее `Python Regular Expressions <https://docs.python.org/3/library/re.html>`_)."
    "commands", "Список строк", "**True**, если текст сообщения совпадает с одной из команд"
    "frm", "От кого обрабатывать события (user, chat, group) по умолчанию user", "**True**, если поле **from_(user, chat, group)** соответственно равно аргументу frm"
    "state", "Состояние автомата", "**True**, если текущее состояние равно состаянию аргумента state"

Чтобы начать обрабатывать события, необходимо запустить ``start_polling()``. Для удобства разработки можно передать параметр ``debug=True``. Тогда все происходящие события будут красиво выводиться в консоль.

#####################
Собственные фильтры
#####################

Чтобы определить собственный фильтр, необходимо написать класс и переопределить функцию ``check``.

.. code-block:: python3

    from vk_maria.dispatcher.filters import AbstractFilter

    class AdminFilter(AbstractFilter):
        def check(self, event: types.Message):
            return event.message.peer_id == 1234567890

И передать его в обработчик события:

.. code-block:: python3

    @dp.message_handler(AdminFilter, commands=['/start'])
    def cmd_start(event: types.Message):
        event.reply("Hi there! What's your name?")

Количество пользовательских фильтров неограничено, их необходимо передавать первым аргументом через запятую.