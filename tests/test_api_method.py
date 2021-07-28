import sys

sys.path.append('../')
from vk_maria.api import ApiMethod

import unittest
import os


should_ship = False

ACCESS_TOKEN = os.environ.get('TOKEN')
if not ACCESS_TOKEN:
    should_ship = True

if not should_ship:
    Api = ApiMethod(access_token=ACCESS_TOKEN, api_version='5.126')


@unittest.skipIf(should_ship, reason='No environment variables configured')
class TestApiMethod(unittest.TestCase):

    def test_send_message(self):
        from random import randint
        group_id = Api('groups.getById')['id']
        r = Api('messages.send', random_id=randint(-100, 100), message='Test message', group_id=group_id, chat_id=9)
        isdigit = isinstance(r, int)
        self.assertEqual(isdigit, True)

    def test_longpoll(self):
        group_id = Api('groups.getById')['id']
        response = Api('groups.getLongPollServer', group_id=group_id)
        server = response['server']
        key = response['key']
        ts = response.get('ts')
        r = Api(server=server, key=key, ts=ts, act='a_check')
        has_updates_and_ts = (r.get('updates') and r.get('ts')) != None
        self.assertEqual(has_updates_and_ts, True)

    def test_upload_files(self):
        with open('test_data/photo.png', 'rb') as file:
            data = {'photo': file.read()}
        group_id = Api('groups.getById')['id']
        upload = Api('photos.getMessagesUploadServer', group_id=group_id)
        r = Api(server=upload['upload_url'], group_id=group_id, files=data)
        has_server_and_photo = (r.get('server') and r.get('photo')) != None
        self.assertEqual(has_server_and_photo, True)