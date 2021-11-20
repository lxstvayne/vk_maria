import typing

from .filters import Filters, FiltersFactory, AbstractFilter
from ..fsm import FSMContext
from ..types import Event


class HandlerObject:
    def __init__(self, function: callable, *filters: AbstractFilter):
        self.function = function
        self.filters = Filters(*filters)

    def test_handler(self, event: Event) -> bool:
        return self.filters.check_all(event)

    def __call__(self, *args):
        if self.function.__code__.co_argcount == 2:
            args = (args[0], FSMContext.get_current())

        return self.function(*args)


class HandlerManager:
    def __init__(self):
        self.handlers: typing.List[HandlerObject] = []

    def register_handler(self,
                         function: callable,
                         *filters,
                         **bound_filters):
        # reg_bound_filters = (FiltersFactory.get_filter_by_key(key, filter_value)
        #                      for key, filter_value in bound_filters.items())

        # reg_filters = (*reg_bound_filters, *(custom_filter() for custom_filter in filters))
        reg_filters = FiltersFactory.get_filters(*filters, **bound_filters)

        self.handlers.append(HandlerObject(function, *reg_filters))
