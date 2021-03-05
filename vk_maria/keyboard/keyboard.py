from .model import Constructor
from .exceptions import *


class Keyboards:
    """
    Объект, через который можно обращаться к клавиатурам из моделей или папки.

    :param models: Файл с моделями клавиатур.
    :param folder: Папка с файлами json клавиатур.
    """

    def __init__(self, models: str = None, folder: str = None):
        self.KEYBOARDS_MODELS = models
        self.KEYBOARDS_FOLDER = folder
        self.keyboards = Constructor(models, folder).kbs

    def __call__(self, keyboard_name):
        try:
            return self.keyboards[keyboard_name]
        except KeyError:
            raise KeyboardNotFoundError('Not found')
