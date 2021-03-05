from .. import working_dir

import json
import inspect
import sys
import os

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

        def __init__(self, app_id: int, owner_id: int, label: str, hash: str, payload: dict):
            self.action = {
                'type': self.type,
                'app_id': app_id,
                'owner_id': owner_id,
                'payload': payload,
                'label': label,
                'hash': hash
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


class Model:
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


class Constructor:

    def unpack_button(self, button):
        if isinstance(button, (Button.Text, Button.Callback)):
            return {
                'action': button.action,
                'color': button.color
            }
        return {
            'action': button.action
        }

    def construct_skeletons(self, cls):
        rows = [row for name, row in cls.__dict__.items() if 'row' in name and row]
        return {
            'inline': cls.inline,
            'one_time': cls.one_time,
            'buttons': [
                [self.unpack_button(button) for button in row] for row in rows
            ]
        }

    def construct_from_files(self):
        k_dir = os.path.join(working_dir, self.folder)

        keyboards = {}
        for file in os.listdir(k_dir):
            keyboards[file.split('.')[0]] = open(os.path.join(k_dir, file)).read()

        return keyboards

    def construct_models(self):
        if self.models:
            module = __import__(self.models)
            keyboard_models = []
            for keyboard in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
                if Model in keyboard[1].__bases__:
                    keyboard_models.append(keyboard[1])

            keyboards = {}
            for keyboard in keyboard_models:
                keyboards[keyboard.__name__] = json.dumps(self.construct_skeletons(keyboard))

            return keyboards

    def __init__(self, models, folder):
        self.models = models
        self.folder = folder
        self.kbs = {}
        if models:
            self.kbs.update(self.construct_models())
        if folder:
            self.kbs.update(self.construct_from_files())
