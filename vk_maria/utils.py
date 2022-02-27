import json
import random
import threading
import time

from pydotdict import DotDict

from .exceptions import VkMariaException
from .keyboard import KeyboardModel
from .keyboard.keyboard import KeyboardMarkup


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
    return random.randint(-2 ** 31, 2 ** 31 - 1)


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


def args_converter(method):
    def wrapper(self, *args, **kwargs):
        for keyword, value in kwargs.items():

            if not value:
                continue

            if keyword == 'peer_ids':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'forward_messages':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'attachment':
                if isinstance(value, str):
                    kwargs[keyword] = value
                elif isinstance(value, list):
                    kwargs[keyword] = ','.join(value)
            elif keyword == 'keyboard':
                if not isinstance(value, str):
                    if isinstance(value, KeyboardMarkup):
                        kwargs[keyword] = value.get_json()
                    elif issubclass(value, KeyboardModel):
                        kwargs[keyword] = value.__json__
            elif keyword == 'cmids':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'fields':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'message_ids':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'media_type':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'name_case':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'market_country':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'market_city':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'obscene_words':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'user_ids':
                kwargs[keyword] = ','.join(str(el) for el in value)
            elif keyword == 'tags':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'keys':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'stories':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'upload_results':
                kwargs[keyword] = ','.join(value)
            elif keyword == 'event_data':
                if isinstance(value, DotDict):
                    value = value.to_dict()
                    kwargs[keyword] = value
                if isinstance(value, dict):
                    kwargs[keyword] = json.dumps(value)

        return method(self, *args, **kwargs)

    return wrapper
