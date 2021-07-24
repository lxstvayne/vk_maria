import inspect
import json
import os
import sys

from .model import Model, construct_json
from .. import working_dir


def get_keyboards_from_files(folder):
    keyboard_dir = os.path.join(working_dir, folder)

    keyboards = {}
    for file in os.listdir(keyboard_dir):
        keyboards[file.split('.')[0]] = open(os.path.join(keyboard_dir, file)).read()

    return keyboards


def get_keyboards_from_models(models):
    module = __import__(models)
    keyboard_models = []
    for keyboard in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
        if Model in keyboard[1].__bases__:
            keyboard_models.append(keyboard[1])

    keyboards = {}
    for keyboard in keyboard_models:
        keyboards[keyboard.__name__] = json.dumps(construct_json(keyboard))

    return keyboards