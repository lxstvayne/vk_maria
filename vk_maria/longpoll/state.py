from .longpoll import LongPoll

__all__ = ('State', 'StatesGroup')


class State:
    def __init__(self, state):
        self._state = state

    @property
    def state(self) -> str:
        return self._state

    def set(self):
        state = LongPoll.get_current().current_context()
        state.set_state(self._state)

    def __eq__(self, other):
        return self.state == other


class StatesGroupMeta(type):
    def __new__(mcs, name, bases, namespace, *args, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)

        states = []
        annotations = namespace.get('__annotations__')
        if annotations:
            for prop_name, prop_cls in annotations.items():
                if issubclass(prop_cls, State):
                    state = State(prop_name)
                    states.append(state)
                    setattr(cls, prop_name, state)

        cls._states = tuple(states)
        cls._state_names = tuple(state.state for state in states)

        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    @classmethod
    def next(cls):
        context = LongPoll.get_current().current_context()
        state = context.get_state()

        try:
            next_step = cls._state_names.index(state) + 1
        except ValueError:
            next_step = 0

        try:
            next_state_name = cls._states[next_step].state
        except IndexError:
            next_state_name = None

        context.set_state(next_state_name)
        return next_state_name

    @classmethod
    def previous(cls) -> str:
        context = LongPoll.get_current().current_context()
        state = context.get_state()

        try:
            previous_step = cls._state_names.index(state) - 1
        except ValueError:
            previous_step = 0

        if previous_step < 0:
            previous_state_name = None
        else:
            previous_state_name = cls._states[previous_step].state_name

        context.set_state(previous_state_name)
        return previous_state_name

    @classmethod
    def first(cls) -> str:
        context = LongPoll.get_current().current_context()
        first_step_name = cls._state_names[0]
        context.set_state(first_step_name)
        return first_step_name

    @classmethod
    def last(cls) -> str:
        context = LongPoll.get_current().current_context()
        last_step_name = cls._state_names[-1]
        context.set_state(last_step_name)
        return last_step_name

    @classmethod
    def finish(cls):
        context = LongPoll.get_current().current_context()
        context.finish()
