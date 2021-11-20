import json
from enum import Enum
from typing import List


class Button:
    """
    Объект описывающий одну из кнопок.
    """

    class Text:
        type = 'text'

        def __init__(self, color: str, label: str, payload: dict = None):
            self.color = color
            self.action = {
                'type': self.type,
                'label': label,
                'payload': payload
            }

    class OpenLink:
        type = 'open_link'

        def __init__(self, link: str, label: str, payload: dict = None):
            self.action = {
                'type': self.type,
                'link': link,
                'label': label,
                'payload': payload

            }

    class Location:
        type = 'location'

        def __init__(self, payload: dict):
            self.action = {
                'type': self.type,
                'payload': payload
            }

    class VKPay:
        type = 'vkpay'

        def __init__(self, payload: dict, hash: str):
            self.action = {
                'type': self.type,
                'payload': payload,
                'hash': hash
            }

    class VKApps:
        type = 'open_app'

        def __init__(self, app_id: int, owner_id: int, label: str, hash: str, payload: dict = None):
            self.action = {
                'type': self.type,
                'app_id': app_id,
                'owner_id': owner_id,
                'label': label,
                'hash': hash,
                'payload': payload
            }

    class Callback:
        type = 'callback'

        def __init__(self, color: str, label: str, payload: dict):
            self.color = color
            self.action = {
                'type': self.type,
                'payload': payload,
                'label': label
            }


class Color(str, Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'


class KeyboardModelMeta(type):
    def __new__(cls, name, bases, namespace):
        if bases:
            namespace['__json__'] = construct_json(namespace)

        return super().__new__(cls, name, bases, namespace)


class KeyboardModel(metaclass=KeyboardModelMeta):
    """
    Объект описывающий клавиатуру.
    """
    inline: bool = False
    one_time: bool = False

    row1: List[Button] = None
    row2: List[Button] = None
    row3: List[Button] = None
    row4: List[Button] = None
    row5: List[Button] = None

    __json__ = None


def unpack_button(button):
    if isinstance(button, (Button.Text, Button.Callback)):
        return {
            'action': button.action,
            'color': button.color
        }
    return {
        'action': button.action
    }


def construct_json(model_dict):
    rows = [row for name, row in model_dict.items() if 'row' in name and row]
    return json.dumps({
        'inline': model_dict.get('inline'),
        'one_time': model_dict.get('one_time'),
        'buttons': [
            [unpack_button(button) for button in row] for row in rows
        ]
    })


class KeyboardMarkup:
    def __init__(self, inline: bool = False, one_time: bool = False):
        self.__current_row = 0
        self.__keyboard_dict__ = {'buttons': [[], ],
                                  'inline': inline,
                                  'one_time': one_time}

    def add_button(self, button):
        self.__keyboard_dict__['buttons'][self.__current_row].append(button)

    def add_row(self):
        self.__current_row += 1
        self.__keyboard_dict__['buttons'].append([])

    def get_json(self):
        __json__ = self.__keyboard_dict__.copy()
        __json__['buttons'] = [[unpack_button(button) for button in row] for row in __json__['buttons'] if row]
        return json.dumps(__json__)
