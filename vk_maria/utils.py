import threading
import time
import random

from .exceptions import VkMariaException


def error_catcher(method):

    def wrapper(self, *args, **kwargs):
        response = method(self, *args, **kwargs)
        e = response[1].get('error')
        if e and e['error_code']:
            raise VkMariaException(e['error_code'], e['error_msg'])

        return response

    return wrapper


def query_delimiter(method):

    def wrapper(self, *args, **kwargs):
        with threading.Lock():
            delay = self.rps_delay - (time.time() - self.last_request)
            if delay > 0:
                time.sleep(delay)
        response = method(self, *args, **kwargs)
        self.last_request = time.time()
        return response

    return wrapper


def get_random_id():
    return random.randint(-2**31, 2**31 - 1)


def response_parser(method):

    # Которые должны получать не список, а 1 объект
    # Только те которые возвращают список из 1 элемента, а не дикт
    fix_methods = [
        'groups.getById',

    ]

    def wrapper(self, *args, **kwargs):

        response = method(self, *args, **kwargs)
        method_, response = response
        if method_ in fix_methods:
            return response['response'][0]

        if not method_:
            return response

        return response['response']

    return wrapper
