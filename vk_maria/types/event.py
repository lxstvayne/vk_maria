from pydotdict import DotDict

from .event_type import EventType


class Event:
    def __init__(self, vk, raw):

        self.vk = vk
        self.fields = {}

        try:
            self.type = EventType(raw['type'])
        except ValueError:
            self.type = raw['type']

        self.fields.update({'type': self.type})

        for k, v in raw['object'].items():
            self.fields.update({k: DotDict(v) if isinstance(v, dict) else v})

        self.__dict__.update(self.fields)

        self.group_id = raw['group_id']

    def __repr__(self):
        return f'<{self.__class__.__name__}({", ".join(f"{k}={v!r}" for k, v in self.fields.items())})>'
