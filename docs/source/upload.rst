:ref: `upload`

Загрузка файлов
-----------------

Класс ``Upload`` реализует готовые функции для загрузки файлов на сервера Вконтакте.

Доступные методы:

* ``photo(photo)``
* ``set_chat_photo(file, chat_id, **kwargs)``
* ``set_group_cover_photo(photo)``
* ``document(document, peer_id, **kwargs)``

Параметры **photo** и **document** могут быть как строкой относительного пути к файлу, так и файлом открытым с помощью **open()** на бинарное чтение **rb** стандартной библиотеки **Python**.