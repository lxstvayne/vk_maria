import pathlib

from ..memory import MemoryStorage

import typing


class FileStorage(MemoryStorage):
    def __init__(self, path: typing.Union[pathlib.Path, str]):
        super().__init__()
        path = self.path = pathlib.Path(path)

        try:
            self.data = self.read(path)
        except FileNotFoundError:
            pass

    def close(self):
        if self.data:
            self.write(self.path)
        super().close()

    def read(self, path: pathlib.Path):
        raise NotImplementedError

    def write(self, path: pathlib.Path):
        raise NotImplementedError
