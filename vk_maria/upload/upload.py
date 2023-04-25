from typing import List

from .utils import prepare_files
from ..api import Vk
from ..types.input_file import InputFile


class Upload:
    """
    Класс реализующий загрузку файлов на сервер вк.
    """

    def __init__(self, vk: Vk):
        self.vk = vk
        self.method = self.vk.method

    def photo(self, photo: InputFile):
        """Загрузка фотографии, возвращает объект для вставки в сообщение"""

        files = prepare_files(photo)
        upload = self.vk.photos_get_messages_upload_server()
        response = self.method(server=upload.upload_url, group_id=upload.group_id, files=files)
        p = self.vk.photos_save_messages_photo(**response)[0]

        return f'photo{p.owner_id}_{p.id}_{p.access_key}'

    def set_chat_photo(self,
                       photo: InputFile,
                       chat_id: int,
                       crop_x: int = None,
                       crop_y: int = None,
                       crop_width: int = None):
        """Установка обложки чата"""

        files = prepare_files(photo)

        upload_url = self.vk.photos_get_chat_upload_server(
            chat_id=chat_id,
            crop_x=crop_x,
            crop_y=crop_y,
            crop_width=crop_width
        )

        response = self.method(server=upload_url, files=files)

        return self.vk.messages_set_chat_photo(file=response['response'])

    def set_group_cover_photo(self,
                              photo: InputFile,
                              crop_x: int = None,
                              crop_y: int = None,
                              crop_x2: int = None,
                              crop_y2: int = None):
        """Загрузка и установка обложки сообщества"""

        files = prepare_files(photo)

        upload_url = self.vk.photos_get_owner_cover_photo_upload_server(
            crop_x=crop_x,
            crop_y=crop_y,
            crop_x2=crop_x2,
            crop_y2=crop_y2
        )

        response = self.method(server=upload_url, files=files)

        return self.vk.photos_save_owner_cover_photo(response['hash'], response['photo'])

    def document(self,
                 document: InputFile,
                 peer_id: int,
                 title: str = None,
                 tags: List[str] = None,
                 return_tags: int = None,
                 type: str = 'doc'):
        """Загрузка документа, возвращает объект для вставки в сообщение"""

        if tags:
            tags = ','.join(tags)

        files = prepare_files(document)

        upload_url = self.vk.docs_get_messages_upload_server(peer_id=peer_id, type=type)
        response = self.method(server=upload_url, files=files)
        d = self.vk.docs_save(file=response['file'], title=title, tags=tags, return_tags=return_tags)

        return f'{d.type}{d.doc["owner_id"]}_{d.doc["id"]}'
