import typing
import inspect
from functools import partial

from .filters import Filters, FiltersFactory, AbstractFilter
from ..fsm import FSMContext
from ...types import Event


class HandlerObject:
    def __init__(self, function: callable, *filters: AbstractFilter):
        self.function = function
        self.filters = Filters(*filters)
        self._bind_args()

    def test_handler(self, event: Event) -> bool:
        return self.filters.check_all(event)

    def _bind_args(self):
        params = inspect.signature(self.function).parameters
        bind_args = {}
        for param_name, annotation in params.items():
            if annotation.annotation == FSMContext:
                bind_args[param_name] = FSMContext.get_current()

        self.function = partial(self.function, **bind_args)

    def __call__(self, *args):
        return self.function(*args)


class HandlerManager:
    def __init__(self):
        self.handlers: typing.List[HandlerObject] = []

    def register_handler(self,
                         function: callable,
                         *filters,
                         **bound_filters):
        reg_filters = FiltersFactory.get_filters(*filters, **bound_filters)
        self.handlers.append(HandlerObject(function, *reg_filters))
