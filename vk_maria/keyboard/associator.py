from .utils import get_keyboards_from_files, get_keyboards_from_models
from .exceptions import *


class KeyboardAssociator:
    """
    Объект, через который можно обращаться к клавиатурам из моделей или папки.

    :param models: Файл с моделями клавиатур.
    :param folder: Папка с файлами json клавиатур.
    """

    def __init__(self, models: str = None, folder: str = None):
        self.KEYBOARDS_MODELS = models
        self.KEYBOARDS_FOLDER = folder
        self.keyboards = {}
        if folder:
            self.keyboards.update(get_keyboards_from_files(folder))
        if models:
            self.keyboards.update(get_keyboards_from_models(models))

    def __getitem__(self, keyboard_name):
        try:
            return self.keyboards[keyboard_name]
        except KeyError:
            raise KeyboardNotFoundError('Not found')
