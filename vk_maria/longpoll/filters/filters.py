import re
import typing
from abc import ABC, abstractmethod

from ..fsm import FSMContext
from ..types import Event, MessageEvent, EventType


class AbstractFilter(ABC):
    @abstractmethod
    def check(self, event: Event):
        return NotImplemented


class BoundFilterMeta(type):
    registered_filters = []

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if cls.__name__ != 'BoundFilter':
            mcs.registered_filters.append(cls)
        return cls


class BoundFilter(metaclass=BoundFilterMeta):
    key: str

    @abstractmethod
    def check(self, event: Event):
        return NotImplemented


class EventTypeFilter(BoundFilter):
    key = 'event_type'

    def __init__(self, event_type: EventType):
        self.event_type = event_type

    def check(self, event: Event):
        if event.type == self.event_type:
            return True
        return False


class TextFilter(BoundFilter):
    key = 'text'

    def __init__(self,
                 equals: str = None,
                 contains: str = None,
                 startswith: str = None,
                 endswith: str = None,
                 ignore_case=False):
        """
        Можно использовать что-то одно из equals, contains, startswith и endswith
        """
        self.equals = equals
        self.contains = contains
        self.startswith = startswith
        self.endswith = endswith
        self.ignore_case = ignore_case

    def check(self, event: MessageEvent):
        text = event.message.text
        if self.ignore_case:
            text = text.lower()

        if self.equals:
            return text == self.equals
        elif self.contains:
            return self.contains in text
        elif self.startswith:
            return text.startswith(self.startswith)
        elif self.endswith:
            return text.endswith(self.endswith)


class CommandsFilter(BoundFilter):
    key = 'commands'

    def __init__(self,
                 commands: typing.List[str],
                 prefixes: str = '',
                 ignore_case: bool = False):
        self.commands = tuple(map(str.lower, commands)) if ignore_case else commands
        self.prefixes = prefixes
        self.ignore_case = ignore_case

    def check(self, event: MessageEvent):
        message_text = event.message.text.lower() if self.ignore_case else event.message.text

        if not message_text:
            return False

        full_command = message_text.split()[0]
        prefix, command = ((full_command[0], full_command[1:])
                           if self.prefixes else (None, full_command))

        if prefix and prefix not in self.prefixes:
            return False

        if command in self.commands:
            return True

        return False


class TypeFromFilter(BoundFilter):
    key = 'frm'

    def __init__(self, frm: str):
        self.frm = frm

    def check(self, event: MessageEvent):
        if getattr(event, f'from_{self.frm}'):
            return True
        return False


class RegexpFilter(BoundFilter):
    key = 'regexp'

    def __init__(self, regexp: str):
        self.regexp = regexp

    def check(self, event: MessageEvent):
        if re.search(self.regexp, event.message.text, re.IGNORECASE):
            return True
        return False


class FSMStateFilter(BoundFilter):
    key = 'state'

    def __init__(self, state: str):
        self.state = state

    def check(self, event: MessageEvent):
        if self.state == FSMContext.get_current().get_state() or self.state == '*':
            return True
        return False


class Filters:
    def __init__(self, *filters: AbstractFilter):
        self.filters: typing.Tuple[AbstractFilter] = filters

    def check_all(self, event: Event) -> bool:
        if all(filter_.check(event) for filter_ in self.filters):
            return True
        return False


class FiltersFactory:
    class UnknownFilterException(Exception):
        pass

    @classmethod
    def get_filters(cls, *custom_filters, **bound_filters):
        filters = (*(cls.get_filter_by_key(key, filter_value)
                     for key, filter_value in bound_filters.items()),
                   *(custom_filter if isinstance(custom_filter, (AbstractFilter, BoundFilter)) else custom_filter()
                     for custom_filter in custom_filters))
        return filters

    @classmethod
    def get_filter_by_key(cls, key: str, filter_value):
        for FILTER_CLASS in BoundFilter.registered_filters:
            if FILTER_CLASS.key == key:
                return FILTER_CLASS(filter_value)

        raise cls.UnknownFilterException(f'Нет подходящего фильтра для `{key}`')
