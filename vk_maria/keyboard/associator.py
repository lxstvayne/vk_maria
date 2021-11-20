import inspect
import os
import sys

from .exceptions import *
from .keyboard import construct_json, KeyboardModel
from .. import working_dir


class KeyboardAssociator:
    """
    Объект, через который можно обращаться к клавиатурам из моделей или папки.

    :param models: Файл с моделями клавиатур.
    :param folder: Папка с файлами json клавиатур.
    """

    @staticmethod
    def get_keyboards_from_files(folder):
        keyboard_dir = os.path.join(working_dir, folder)

        keyboards = {}
        for file in os.listdir(keyboard_dir):
            keyboards[file.split('.')[0]] = open(os.path.join(keyboard_dir, file)).read()

        return keyboards

    @staticmethod
    def get_keyboards_from_models(models):
        module = __import__(models)
        keyboard_models = []
        for keyboard in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
            if KeyboardModel in keyboard[1].__bases__:
                keyboard_models.append(keyboard[1])

        keyboards = {}
        for keyboard in keyboard_models:
            keyboards[keyboard.__name__] = construct_json(keyboard.__dict__)

        return keyboards

    def __init__(self, models: str = None, folder: str = None):
        self.KEYBOARDS_MODELS = models
        self.KEYBOARDS_FOLDER = folder
        self.keyboards = {}
        if folder:
            self.keyboards.update(self.get_keyboards_from_files(folder))
        if models:
            self.keyboards.update(self.get_keyboards_from_models(models))

    def __getitem__(self, keyboard_name):
        try:
            return self.keyboards[keyboard_name]
        except KeyError:
            raise KeyboardNotFoundError('Not found')

    def __getattr__(self, keyboard_name):
        return self.__getitem__(keyboard_name)
