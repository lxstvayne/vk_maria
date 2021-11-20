from os import PathLike
from typing import Union, List, BinaryIO

from .utils import open_files
from ..api import Vk


class Upload:
    """
    Класс реализующий загрузку файлов на сервер вк.
    """
    def __init__(self, vk: Vk):
        self.vk = vk
        self.method = self.vk.method

    def photo(self, photo: Union[str, bytes, PathLike]):
        """Загрузка фотографии, возвращает объект для вставки в сообщение"""

        data = open_files(photo, 'photo')

        upload = self.vk.photos_get_messages_upload_server()
        response = self.method(server=upload.upload_url, group_id=upload.group_id, files=data)
        p = self.vk.photos_save_messages_photo(**response)[0]

        return f'photo{p.owner_id}_{p.id}_{p.access_key}'

    def set_chat_photo(self,
                       photo: Union[str, bytes, PathLike],
                       chat_id: int,
                       crop_x: int = None,
                       crop_y: int = None,
                       crop_width: int = None):
        """Установка обложки чата"""

        data = open_files(photo, 'photo')

        upload_url = self.vk.photos_get_chat_upload_server(
            chat_id=chat_id,
            crop_x=crop_x,
            crop_y=crop_y,
            crop_width=crop_width
        )

        response = self.method(server=upload_url, files=data)

        return self.vk.messages_set_chat_photo(file=response['response'])

    def set_group_cover_photo(self,
                              photo: Union[str, bytes, PathLike],
                              crop_x: int = None,
                              crop_y: int = None,
                              crop_x2: int = None,
                              crop_y2: int = None):
        """Загрузка и установка обложки сообщества"""

        data = open_files(photo, 'photo')

        upload_url = self.vk.photos_get_owner_cover_photo_upload_server(
            crop_x=crop_x,
            crop_y=crop_y,
            crop_x2=crop_x2,
            crop_y2=crop_y2
        )

        response = self.method(server=upload_url, files=data)

        return self.vk.photos_save_owner_cover_photo(response['hash'], response['photo'])

    def document(self,
                 document: Union[str, BinaryIO, PathLike, List[Union[str, BinaryIO, PathLike]]],
                 peer_id: int,
                 title: str = None,
                 tags: List[str] = None,
                 return_tags: int = None,
                 type: str = 'doc'):
        """Загрузка документа, возвращает объект для вставки в сообщение"""

        if tags:
            tags = ','.join(tags)

        data = open_files(document, 'file')

        upload_url = self.vk.docs_get_messages_upload_server(peer_id=peer_id, type=type)
        response = self.method(server=upload_url, files=data)
        d = self.vk.docs_save(file=response['file'], title=title, tags=tags, return_tags=return_tags)

        return f'{d.type}{d.doc["owner_id"]}_{d.doc["id"]}'
