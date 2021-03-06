# <p align="center">vk_maria

<p align="center">Простая в использовании

* [Установка](#установка)
* [Ваш первый бот](#ваш-первый-бот)
    * [Предисловие](#предисловие)
    * [Простейший эхо бот](#простейший-эхо-бот)
* [Общая документация по библиотеке](#общая-документация-по-библиотеке)
    * [Vk](#vk)
    * [LongPoll](#longpoll)
    * [Обработчики событий](#обработчики-событий)
    * [EventType](#eventtype)
    * [Upload](#upload)
    * [Клавиатуры](#клавиатуры)
        * [Keyboards](#keyboards)
        * [Model](#model)
        * [Button](#button)
* [Постскриптум ](#постскриптум )
## Установка

* Установка с помощью pip:
```
$ pip install vk_maria
```
* Установка с github:
```
$ git clone https://github.com/lxstvayne/vk_maria
$ cd vk_maria
$ python setup.py install
```
Обычно рекомендуется использовать первый способ.

*Хотя библиотека и готова к использованию, она всё ещё находится на стадии разработки, поэтому не забывайте регулярно её обновлять `pip install vk_maria --upgrade`*

## Ваш первый бот

### Предисловие

В примерах `token` предполагает [ключ доступа](https://vk.com/dev/access_token) вашего сообщества.

### Простейший эхо бот

Класс `Vk` инкапсулирует все методы работы с токеном сообщества. Класс `LongPoll` предоставляет возможность работы с событиями сообщества.

Создайте файл `echo_bot.py`. Откройте его и создайте экземпляр класса `Vk`:
```python
from vk_maria import Vk, LongPoll


vk = Vk(access_token='token')
```
*Примечание: Обязательно замените `token` ключом доступа вашего сообщества.*

Затем создайте экземпляр класса `LongPoll` передав ему в качестве аргумента `vk`:
```python
longpoll = LongPoll(vk)
```
После этого нам необходимо зарегистрировать обработчик событий. Обработчики событий определяют фильтры, которые должно пройти событие. Если событие проходит фильтры, вызывается декорированная функция и входящее событие передаётся в качестве аргумента.

Давайте определим обработчик событий, который будет обрабатывать все входящие сообщения от пользователя в личные сообщения сообщества и отвечать на команду *Начать*:
```python
@longpoll.message_handler(commands='Начать')
def send_welcome(event):
    vk.messages_send(user_id=event.message.from_id, message='Добро пожаловать!')
```
Добавим ещё один обработчик:
```python
@longpoll.message_handler()
def echo(event):
    vk.messages_send(user_id=event.message.from_id, message=event.message.text)
```
Декорированная функция может иметь произвольное имя, однако она должна принимать только 1 параметр (event).

*Примечание: все обработчики тестируются в том порядке, в котором они были объявлены.*

Отлично, теперь у нас есть простой бот, который отвечает на сообщение *Начать* приветствием и повторяет остальные отправленные сообщения. Чтобы запустить бота добавьте в исходный код следующее:
```python
longpoll.polling()
```
Вот и всё! Наш исходный файл теперь выглядит так:
```python
from vk_maria import Vk, LongPoll


vk = Vk(access_token='token')
longpoll = LongPoll(vk)

@longpoll.message_handler(commands='Начать')
def send_welcome(event):
    vk.messages_send(user_id=event.message.from_id, message='Добро пожаловать!')

@longpoll.message_handler()
def echo(event):
    vk.messages_send(user_id=event.message.from_id, message=event.message.text)


longpoll.polling()
```
Чтобы запустить бота, просто откройте терминал, введите `python echo_bot.py` и протестируйте его.

## Общая документация по библиотеке

Все инструменты импортируются исключительно из пакета `vk_maria`.

Доступные инструменты:
* `Vk`
* `LongPoll`
* `EventType`
* `Upload`
* `Keyboards`
* `Model`
* `Button`
___
### Vk

`Vk`, как говорилось раннее, инкапсулирует [все методы](https://vk.com/dev/methods) для работы при помощи ключа доступа сообщества.
___
### LongPoll

Экземпляр класса `LongPoll` позволяет обрабатывает события в сообществе. Он предоставляет обработку как через цикл:
```python
for event in longpoll.listen():
    ...
```
Так и через удобный декоратор `message_handler`:
```python
@longpoll.message_handler()
def do_smth(event):
    ...

longpoll.polling()
```
___
#### Обработчики событий

Обработчик событий это функция с декоратором `message_handler()`. Он определяет фильтры для обрабатываемых событий.

```python
@longpoll.message_handler(**filters)
def do_smth(event):
    ...
```
Фильтр объявляется следующим образом `name=argument`.

Доступные фильтры:

|Название|Аргументы|Условие|
|:---:|---| ---|
|type|Тип события из EventType по умолчанию MESSAGE_NEW.|`True`, если типы событий совпадают.|
|regexp|Регулярное выражение или подстрока.|`True`, если подстрока находится в сообщении или строка проходит проверку на наличие шаблона регулярного выражения (Подробнее [Python Regular Expressions](https://docs.python.org/2/library/re.html)).|
|commands|Список с командами.|`True`, если текст сообщения совпадает с одной из команд.|
|frm |От кого обрабатывать события (`'user'`, `'chat'`, `'group'`)  по умолчанию `'user'`.|`True`, если поле from_(`user`, `chat`, `group`) соответсвенно `True`.

Чтобы начать обрабатывать события, необходимо запустить `polling()`. Для удобства разработки можно передать параметр `debug=True`. Тогда все происходящие события будут красиво выводиться в консоль.

___
### EventType

`EventType` представляет из себя перечисление всех возможных событий. К примеру `MESSAGE_NEW`, `MESSAGE_TYPING_STATE`, `MESSAGE_REPLY`...
___
### Upload

Класс `Upload` реализует готовые функции для загрузки файлов на сервера Вконтакте.

Доступные методы:
* `photo(photo)`
* `set_chat_photo(file, chat_id, **kwargs)`
* `set_group_cover_photo(photo)`
* `document(document, peer_id, **kwargs)`

Параметры `photo` и `document` могут быть как строкой относительного пути к файлу, так и файлом открытым с помощью `open()` на бинарное чтение `rb` стандартной библиотеки `Python`.
___
## Клавиатуры

Вы можете использовать ассоциации для отправки клавиатур.

### Keyboards

Чтобы создать ассоциации клавиатур необходимо создать экземпляр класса `Keyboards`:
```python
kbs = Keyboards(folder='keyboards', models='models')
```
* `folder` - папка с файлами клавиатур в формате `json`;
* `models` - файл с расширением `.py`, хранящий модели клавиатур.

Теперь вы можете получать клавиатуру вызвав `kbs(keyboard)`, где `keyboard` - название вашей клавиатуры. 

### Model

С помощью класса `Model` можно удобно создавать свои клавиатуры на `Python`.

Пример:

Создадим файл `keyboards.py`, где будут храниться наши модели. Импортируем `Model` и `Button`:
```python
from vk_maria import Model, Button
```
Теперь необходимо определить свои модели. Для этого необходимо создать классы, родителями которых будет `Model`:
```python
class TestKeyboard(Model):

    one_time = True

    row1 = [
        Button.Text(color='primary', label='Кнопка 1'), Button.Text(color='primary', label='Кнопка 2')
    ]
    row2 = [
        Button.Text(color='primary', label='Кнопка 3'), Button.Text(color='primary', label='Кнопка 4')
    ]


class Calculator(Model):

    row1 = [
        Button.Text(color='primary', label='1'),
        Button.Text(color='primary', label='2'),
        Button.Text(color='primary', label='3')
    ]

    row2 = [
        Button.Text(color='primary', label='4'),
        Button.Text(color='primary', label='5'),
        Button.Text(color='primary', label='6')
    ]

    row3 = [
        Button.Text(color='primary', label='7'),
        Button.Text(color='primary', label='8'),
        Button.Text(color='primary', label='9')
    ]

    row4 = [
        Button.Text(color='primary', label='0')
    ]


class Empty(Model):
    pass
```
Теперь необходимо создать объект типа `Keyboards` и указать в нём название файла с нашими моделями:
```python
kbs = Keyboards(models='keyboards')
```
Готово! Мы можем обращаться к нашим объектам клавиатур через `kbs`:
```python
vk.messages_send(user_id='yourid', message='Разовая клавиатура', keyboard=kbs('TestKeyboard')
vk.messages_send(user_id='yourid', message='Инлайн клавиатура', keyboard=kbs('Calculator')
```
Если необходимо скрыть клавиатуру у пользователя, отправьте пустую модель:
```python
vk.messages_send(user_id='yourid', message='Скрываю клавиатуру', keyboard=kbs('Empty')
```

### Button

Содержит объекты кнопок:
* `Text`
* `OpenLink`
* `Location`
* `VKPay`
* `VKApps`
* `Callback`

Подробнее о них вы можете прочитать в [официальной документации](https://vk.com/dev/bots_docs_3?f=4.2.%20%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85)

## Постскриптум

Я старался написать простую и удобную библиотеку.
Если у вас есть идеи по её улучшению, вы можете отправить письмо мне на почту lxstv4yne@gmail.com.
