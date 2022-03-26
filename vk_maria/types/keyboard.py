import enum
import json
import typing
from typing import List


class BaseButton:
    type: str
    action: dict


class TextButton(BaseButton):
    type = 'text'

    def __init__(self, color: str, label: str, payload: dict = None):
        self.color = color
        self.action = {
            'type': self.type,
            'label': label,
            'payload': payload
        }


class OpenLinkButton(BaseButton):
    type = 'open_link'

    def __init__(self, link: str, label: str, payload: dict = None):
        self.action = {
            'type': self.type,
            'link': link,
            'label': label,
            'payload': payload

        }


class LocationButton(BaseButton):
    type = 'location'

    def __init__(self, payload: dict):
        self.action = {
            'type': self.type,
            'payload': payload
        }


class VKPayButton(BaseButton):
    type = 'vkpay'

    def __init__(self, payload: dict, hash_: str):
        self.action = {
            'type': self.type,
            'payload': payload,
            'hash': hash_
        }


class VKAppsButton(BaseButton):
    type = 'open_app'

    def __init__(self, app_id: int, owner_id: int, label: str, hash_: str, payload: dict = None):
        self.action = {
            'type': self.type,
            'app_id': app_id,
            'owner_id': owner_id,
            'label': label,
            'hash': hash_,
            'payload': payload
        }


class CallbackButton(BaseButton):
    type = 'callback'

    def __init__(self, color: str, label: str, payload: dict):
        self.color = color
        self.action = {
            'type': self.type,
            'payload': payload,
            'label': label
        }


class Button:
    Text = TextButton
    OpenLink = OpenLinkButton
    Location = LocationButton
    VKPay = VKPayButton
    VKApps = VKAppsButton
    Callback = CallbackButton


class Color(str, enum.Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'


class KeyboardModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if bases:
            namespace['__json__'] = construct_json(namespace)

        return super().__new__(mcs, name, bases, namespace)


class KeyboardModel(metaclass=KeyboardModelMeta):
    inline: bool = False
    one_time: bool = False

    row1: List[Button] = None
    row2: List[Button] = None
    row3: List[Button] = None
    row4: List[Button] = None
    row5: List[Button] = None
    # ... etc rows

    __json__ = None


def unpack_button(button: BaseButton):
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
    def __init__(self,
                 inline: bool = False,
                 one_time: bool = False,
                 keyboard: typing.List[typing.List[BaseButton]] = None):
        self.__current_row = 0
        keyboard = [[], ] or keyboard
        self.__keyboard_dict__ = {'buttons': keyboard,
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


RemoveReplyMarkup = KeyboardMarkup()
