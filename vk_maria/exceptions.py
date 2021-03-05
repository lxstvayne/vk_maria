class UnknownError(Exception):
    pass


class UnknownMethodError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class PermissionError(Exception):
    pass


class WrongRequestError(Exception):
    pass


class ServerError(Exception):
    pass


class AccessIsDeniedError(Exception):
    pass


class DeprecatedMethodError(Exception):
    pass


class InvalidParametersError(Exception):
    pass


class KeyIsNotValidError(Exception):
    pass


class VkMariaException:
    exceptions = {
        1: UnknownError,
        3: UnknownMethodError,
        5: AuthorizationError,
        7: PermissionError,
        8: WrongRequestError,
        10: ServerError,
        15: AccessIsDeniedError,
        23: DeprecatedMethodError,
        27: KeyIsNotValidError,
        100: InvalidParametersError
    }

    def __init__(self, code: int, text: str):
        if code in self.exceptions:
            raise self.exceptions[code](text)
        raise Exception(text)
