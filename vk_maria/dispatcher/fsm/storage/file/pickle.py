import pathlib
import pickle

from .base import FileStorage


class PickleStorage(FileStorage):
    """
    Pickle File storage based on MemoryStorage
    """

    def read(self, path: pathlib.Path):
        if not pathlib.Path(path).exists():
            with path.open('wb+') as f:
                pickle.dump({}, f, protocol=pickle.HIGHEST_PROTOCOL)
            return {}

        with path.open('rb') as f:
            return pickle.load(f)

    def write(self, path: pathlib.Path):
        with path.open('wb') as f:
            return pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)
