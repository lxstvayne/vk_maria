from vk_maria import Vk, Upload


def main():
    """Пример загрузки и отправки фотографии в личное сообщение"""

    vk = Vk(access_token='token')
    upload = Upload(vk)

    photo = upload.photo('your_photo.png') # Или upload.photo(open('your_photo.png', 'rb'))

    vk.messages_send(user_id=121930743, attachment=photo)


if __name__ == '__main__':
    main()
