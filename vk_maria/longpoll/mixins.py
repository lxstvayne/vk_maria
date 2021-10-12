

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_current(cls):
        return cls._instances[cls]


class ContextInstanceMixin(metaclass=Singleton):
    pass

