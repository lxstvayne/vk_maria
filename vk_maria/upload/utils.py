from _io import BufferedReader
from typing import Union, List, BinaryIO

from .exceptions import *
from .. import working_dir


def open_file(file: Union[str, BinaryIO]):

    if isinstance(file, BufferedReader):
        file = file
    elif isinstance(file, str):
        file = open(working_dir + '/' + file, 'rb')
    else:
        raise InvalidFileFormatError('Неверный формат файла')

    return file


def open_files(files: Union[str, BinaryIO, List[Union[str, BinaryIO]]], type: str):

    if isinstance(files, list) and len(files) > 1:
        data = {f'{type}{i}': open_file(f) for i, f in enumerate(files, start=1)}
    else:
        data = {type: open_file(files)}

    return data
