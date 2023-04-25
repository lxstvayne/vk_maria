from vk_maria import Vk, types
from vk_maria.upload import Upload


def main():
    """Пример загрузки и отправки фотографии в личное сообщение"""

    vk = Vk(access_token='TOKEN')
    upload = Upload(vk)

    image = types.FileSystemInputFile('./image.jpg')
    # Or
    # image = types.BufferedInputFile(filename, BytesIO)
    photo = upload.photo(image)

    vk.messages_send(user_id=1234567890, attachment=photo)


if __name__ == '__main__':
    main()