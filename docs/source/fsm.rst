:ref: `fsm`

Конечные автоматы (FSM)
------------------------

Если вашему боту необходима система диалогов, то в дело вступают конечные автоматы. Это некая математическая модель, которая представляет собой набор состояний, которые переключаются в определённых условиях. В библиотеке это реализовано с помощью классов

.. code-block:: python3

    from vk_maria.dispatcher.fsm import StatesGroup, State, MemoryStorage, FSMContext

    class Form(StatesGroup):
        waiting_for_name: State
        waiting_for_age: State
        waiting_for_gender: State


Необходимо описать в классе переменные состояний.

Чтобы имелась возможность запоминать текущие состояния для диалогов всех пользователей, в класс ``Dispatcher`` необходимо передать экземпляр хранилища состояний.

.. code-block:: python3

    dp = Dispatcher(vk, MemoryStorage())


В библиотеке на данный момент реализованы следующие хранилища состояний: ``MemoryStorage``, ``JSONStorage``, ``PickleStorage``.


#######################
Пример реализации
#######################

.. code-block:: python3

    from vk_maria import Vk, types
    from vk_maria.dispatcher import Dispatcher
    from vk_maria.dispatcher.fsm import StatesGroup, State, MemoryStorage, FSMContext
    from vk_maria.types import KeyboardMarkup, Button, Color, RemoveReplyMarkup


    vk = Vk(access_token='token')
    dp = Dispatcher(vk, MemoryStorage())

    GENDERS = ('Male', 'Female', 'Other')


    class Form(StatesGroup):
        waiting_for_name: State
        waiting_for_age: State
        waiting_for_gender: State


    @dp.message_handler(commands=['/start'])
    def cmd_start(event: types.Message):
        event.reply("Hi there! What's your name?")
        Form.waiting_for_name.set()


    @dp.message_handler(state=Form.waiting_for_name)
    def process_name(event: types.Message, state: FSMContext):
        state.update_data(name=event.message.text)
        event.reply("How old are you?")
        Form.next()


    @dp.message_handler(state=Form.waiting_for_age)
    def process_age(event: types.Message, state: FSMContext):
        state.update_data(age=event.message.text)

        markup = KeyboardMarkup(one_time=False)
        for gender in GENDERS:
            markup.add_button(Button.Text(Color.PRIMARY, gender))

        event.reply('What is your gender?', keyboard=markup)
        Form.next()


    @dp.message_handler(state=Form.waiting_for_gender)
    def process_gender(event: types.Message, state: FSMContext):
        if event.message.text not in GENDERS:
            return event.reply('Bad gender name. Choose your gender from the keyboard.')

        state.update_data(gender=event.message.text)
        user_data = state.get_data()
        event.answer(f'Hi! Nice to meet you, {user_data["name"]}\n'
                     f'Age: {user_data["age"]}\n'
                     f'Gender: {user_data["gender"]}', keyboard=RemoveReplyMarkup)
        Form.finish()


    if __name__ == '__main__':
        dp.start_polling(debug=True)


.. note:: Чтобы каждый раз не писать FSMContext.get_current(), можно передать аргумент state: FSMContext в функцию-обработчик.

Чтобы отлавливать состояние, передаётся аргумент ``state`` для ``message_handler``

