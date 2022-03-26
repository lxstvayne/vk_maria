from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.dispatcher.fsm import StatesGroup, State, MemoryStorage, FSMContext
from vk_maria.keyboard import KeyboardMarkup, Button, Color, EmptyKeyboard


vk = Vk(access_token='token')
lp = Dispatcher(vk, MemoryStorage())

GENDERS = ('Male', 'Female', 'Other')


class Form(StatesGroup):
    waiting_for_name: State
    waiting_for_age: State
    waiting_for_gender: State


@lp.message_handler(commands=['/start'])
def cmd_start(event: types.Message):
    event.reply("Hi there! What's your name?")
    Form.waiting_for_name.set()


@lp.message_handler(state=Form.waiting_for_name)
def process_name(event: types.Message, state: FSMContext):
    state.update_data(name=event.message.text)
    event.reply("How old are you?")
    Form.next()


@lp.message_handler(state=Form.waiting_for_age)
def process_age(event: types.Message, state: FSMContext):
    state.update_data(age=event.message.text)

    markup = KeyboardMarkup(one_time=False)
    for gender in GENDERS:
        markup.add_button(Button.TextButton(Color.PRIMARY, gender))

    event.reply('What is your gender?', keyboard=markup)
    Form.next()


@lp.message_handler(state=Form.waiting_for_gender)
def process_gender(event: types.Message, state: FSMContext):
    if event.message.text not in GENDERS:
        return event.reply('Bad gender name. Choose your gender from the keyboard.')

    state.update_data(gender=event.message.text)
    user_data = state.get_data()
    event.answer(f'Hi! Nice to meet you, {user_data["name"]}\n'
                 f'Age: {user_data["age"]}\n'
                 f'Gender: {user_data["gender"]}', keyboard=EmptyKeyboard)
    Form.finish()


if __name__ == '__main__':
    lp.start_polling(debug=True)

