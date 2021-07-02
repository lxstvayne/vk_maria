import threading
import time
import random

from .keyboard import Model
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


def args_converter(method):

    def wrapper(self, *args, **kwargs):
        args_dict = kwargs
        if args_dict.get('peer_ids'):
            args_dict['peer_ids'] = ','.join(str(el) for el in args_dict['peer_ids'])
        if args_dict.get('forward_messages'):
            args_dict['forward_messages'] = ','.join(str(el) for el in args_dict['forward_messages'])
        if args_dict.get('keyboard') and not isinstance(args_dict.get('keyboard'), str) and issubclass(args_dict.get('keyboard'), Model):
            args_dict['keyboard'] = args_dict['keyboard'].to_json()
        if args_dict.get('fields'):
            args_dict['fields'] = ','.join(args_dict['fields'])
        if args_dict.get('message_ids'):
            args_dict['message_ids'] = ','.join(str(el) for el in args_dict['message_ids'])
        if args_dict.get('media_type'):
            args_dict['media_type'] = ','.join(args_dict['media_type'])
        if args_dict.get('name_case'):
            args_dict['name_case'] = ','.join(args_dict['name_case'])
        if args_dict.get('market_country'):
            args_dict['market_country'] = ','.join(str(el) for el in args_dict['market_country'])
        if args_dict.get('market_city'):
            args_dict['market_city'] = ','.join(str(el) for el in args_dict['market_city'])
        if args_dict.get('obscene_words'):
            args_dict['obscene_words'] = ','.join(args_dict['obscene_words'])
        if args_dict.get('user_ids'):
            args_dict['user_ids'] = ','.join(str(el) for el in args_dict['user_ids'])
        if args_dict.get('tags'):
            args_dict['tags'] = ','.join(args_dict['tags'])
        if args_dict.get('keys'):
            args_dict['keys'] = ','.join(args_dict['keys'])
        if args_dict.get('stories'):
            args_dict['stories'] = ','.join(args_dict['stories'])
        if args_dict.get('upload_results'):
            args_dict['upload_results'] = ','.join(args_dict['upload_results'])

        return method(self, *args, **args_dict)

    return wrapper