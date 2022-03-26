import json
import pathlib

from .base import FileStorage


class JSONStorage(FileStorage):
    """
    JSON File storage based on MemoryStorage
    """

    def read(self, path: pathlib.Path):
        if not pathlib.Path(path).exists():
            with path.open('w+') as f:
                json.dump({}, f, indent=4)
            return {}

        with path.open('r') as f:
            return json.load(f, object_hook=lambda d: {int(k)
                                                       if k.lstrip('-').isdigit() else k: v
                                                       for k, v in d.items()})

    def write(self, path: pathlib.Path):
        with path.open('w') as f:
            print(self.data)
            return json.dump(self.data, f, indent=4)
