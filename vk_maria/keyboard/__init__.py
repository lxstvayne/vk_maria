from .associator import KeyboardAssociator
from .keyboard import KeyboardModel, KeyboardMarkup, Button, Color


class EmptyKeyboard(KeyboardModel):
    pass


def gen_keyboard(keyboard_name: str, keyboard: dict) -> str:
    """
    Возвращает класс клавиатуры из json.
    """
    button_by_type = {
        'text': lambda color, label, payload="{}": f'Button.Text("{color}", "{label}", {payload})',
        'open_link': lambda link, label, payload="{}": f'Button.OpenLink("{link}", "{label}", {payload})',
        'location': lambda payload="{}": f'Button.Location({payload})',
        'vkpay': lambda payload, hash: f'Button.VKPay({payload}, "{hash}")',
        'open_app': lambda app_id, owner_id, label, hash, payload="{}": f'Button.VKApps({app_id}, {owner_id}, "{label}", "{hash}", {payload})',
        'callback': lambda color, label, payload="{}": f'Button.Callback("{color}", "{label}", {payload})'
    }
    inline = keyboard.get('inline', False)
    one_time = keyboard.get('one_time', False)
    keyboard_class = (f'class {keyboard_name}(Model):\n'
                      f'\tinline = {inline}\n'
                      f'\tone_time = {one_time}\n\n')

    for row_number, btn_row in enumerate(keyboard['buttons'], 1):
        row = '[\n'
        for btn in btn_row:
            type = btn['action']['type']
            btn.update(btn['action'])
            btn.pop('action')
            btn.pop('type')
            if btn.get('payload') == "":
                btn.pop('payload')
            row += f'\t\t{button_by_type[type](**btn)},\n'
        row += '\t]'

        keyboard_class += f'\trow{row_number} = {row}\n\n'
    return keyboard_class


def gen_single_keyboard_from_json(filename: str) -> str:
    """
    Возвращает сгенерированный модуль вашей клавиатуры.
    """
    import json
    with open(file=filename) as file:
        keyboard = json.load(file)

    result = ('from vk_maria.keyboard import Model, Button\n\n\n')
    return result + gen_keyboard('MyKeyboard', keyboard).strip()


def gen_keyboards_from_folder(folder: str, module_name: str = 'my_keyboards') -> None:
    """
    Генерирует модуль с собранными классами ваших клавиатур.
    """
    import glob, json
    result = ('from vk_maria.keyboard import Model, Button\n\n\n')
    for file in glob.glob(f'{folder}/*.json'):
        keyboard_name = file.split('\\')[-1].split('.')[0]
        with open(file, 'rb') as file:
            keyboard = json.load(file)
        result += gen_keyboard(keyboard_name.title(), keyboard)

    with open(f'{module_name}.py', 'w+') as file:
        file.write(result.strip())