import io
import os.path
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class InputFile(ABC):
    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def read(self):
        pass


class BufferedInputFile(InputFile):
    def __init__(self, filename: str, buffer: io.BytesIO):
        super().__init__(filename=filename)

        self.buffer = buffer

    def read(self):
        return self.buffer.read()


class FileSystemInputFile(InputFile):
    def __init__(self, path: Union[str, Path]):
        filename = os.path.basename(path)
        super().__init__(filename=filename)

        self.path = path

    def read(self):
        with open(self.path, 'rb') as f:
            return f.read()
