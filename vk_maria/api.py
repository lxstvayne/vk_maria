import requests

from .responses import *
from .utils import error_catcher, query_delimiter, get_random_id, response_parser, args_converter


class ApiMethod:
    base_url: str = 'https://api.vk.com/method/'
    http = requests.Session()
    rps_delay = 0.05
    last_request = 0.0

    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version

    @response_parser
    @error_catcher
    @query_delimiter
    @args_converter
    def __call__(self, method: str = None, server: str = None, files=None, **kwargs):
        if files:
            response = self.http.post(server, files=files, timeout=90).json()
        elif not method:
            response = self.http.post(server, data=kwargs, files=files, timeout=90).json()
        else:
            url = self.base_url + method
            response = self.http.post(
                url,
                data=dict(access_token=self.access_token, v=self.api_version, server=server, **kwargs),
                timeout=90
            ).json()

        return method, response


class Vk:
    """
    Читайте подробнее про методы https://vk.com/dev/methods

    :param access_token: Токен сообщества
    :param api_version: Версия Api
    """

    def __init__(self, access_token: str, api_version: str = '5.126'):
        self.method = ApiMethod(access_token=access_token, api_version=api_version)
        self.group_id = GroupsGetById(self.method(method='groups.getById')).id

    def messages_create_chat(self, user_ids: List[int], title: str):
        """
        :param user_ids: Идентификаторы пользователей, которых нужно включить в мультидиалог.
        :param title: Название беседы.
        """

        user_ids = ','.join(str(el) for el in user_ids)

        return self.method('messages.createChat', group_id=self.group_id, user_ids=user_ids, title=title)

    def messages_delete(self, message_ids: List[int] = None,
                        peer_id: int = None,
                        spam: int = None,
                        delete_for_all: int = None,
                        cmids: List[int] = None):
        """
        :param message_ids: Список идентификаторов сообщений.
        :param spam: Помечает сообщения как спам.
        :param delete_for_all: Удаление для всех.
        :param cmids: Conversation Message Ids
        """
        return self.method('messages.delete', group_id=self.group_id, message_ids=message_ids,
                           spam=spam, delete_for_all=delete_for_all, cmids=cmids, peer_id=peer_id)

    def messages_delete_chat_photo(self, chat_id: int):
        """
        :param chat_id: Идентификатор беседы.
        """
        return MessagesDeleteChatPhoto(
            self.method('messages.deleteChatPhoto', group_id=self.group_id, chat_id=chat_id)
        )

    def messages_delete_conversation(self, user_id: int = None, peer_id: int = None):
        """
        :param user_id: Идентификатор пользователя.
                        Если требуется очистить историю беседы, используйте peer_id.

        :param peer_id: Идентификатор назначения.
        """
        return MessagesDeleteConversation(
            self.method('messages.deleteConversation', group_id=self.group_id, user_id=str(user_id), peer_id=peer_id)
        )

    def messages_edit(self, peer_id: int, message: str = None, lat: float = None, long: float = None, attachment=None,
                      keep_forward_messages: int = None, keep_snippets: int = None, dont_parse_links: int = None,
                      message_id: int = None, conversation_message_id: int = None, template=None, keyboard=None):
        """
        :param peer_id: Идентификатор назначения.
        :param message: Текст сообщения. Обязательный параметр, если не задан параметр attachment.
        :param lat: Географическая широта (от -90 до 90).
        :param long: Географическая долгота (от -180 до 180).
        :param attachment: Медиавложения к личному сообщению, перечисленные через запятую.
        :param keep_forward_messages: Сохранить прикреплённые пересланные сообщения.
        :param keep_snippets: Сохранить прикреплённые внешние ссылки (сниппеты).
        :param dont_parse_links: Не создавать сниппет ссылки из сообщения.
        :param message_id: Идентификатор сообщения.
        :param conversation_message_id: Идентификатор сообщения в беседе.
        :param template: Объект, описывающий шаблоны сообщений.
        :param keyboard: Объект, описывающий клавиатуру бота.
        """
        return self.method('messages.edit', group_id=self.group_id, peer_id=peer_id, message=message, lat=lat,
                           long=long, attachment=attachment, keep_forward_messages=keep_forward_messages,
                           keep_snippets=keep_snippets, dont_parse_links=dont_parse_links, message_id=message_id,
                           template=template, keyboard=keyboard, conversation_message_id=conversation_message_id)

    def messages_edit_chat(self, chat_id: int, title: str):
        """
        :param chat_id: Идентификатор беседы.
        :param title: Новое название для беседы.
        """
        return self.method('messages.editChat', chat_id=chat_id, title=title)

    def messages_get_by_conversation_message_id(self, peer_id: int, conversation_message_ids: List[int],
                                                extended: int = None, fields: List[str] = None):
        """
        :param peer_id: Идентификатор назначения.
        :param conversation_message_ids: Идентификаторы сообщений. Максимум 100 идентификаторов.
        :param extended: Возвращать дополнительные поля.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetByConversationMessageId(
            self.method(
                'messages.getByConversationMessageId', group_id=self.group_id, peer_id=peer_id,
                conversation_message_ids=conversation_message_ids, extended=extended, fields=fields)
        )

    def messages_get_by_id(self, message_ids: List[int], preview_length: int = None,
                           extended: int = None, fields: List[str] = None):
        """
        :param message_ids: Идентификаторы сообщений. Максимум 100 идентификаторов.
        :param preview_length: Количество символов, по которому нужно обрезать сообщение.
        :param extended: Возвращать дополнительные поля.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetById(
            self.method('messages.getById', group_id=self.group_id, message_ids=message_ids,
                        preview_length=preview_length, extended=extended, fields=fields)
        )

    def messages_get_conversation_members(self, peer_id: int, fields: List[str]):
        """
        :param peer_id: Идентификатор назначения.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetConversationMembers(
            self.method('messages.getConversationMembers', group_id=self.group_id, peer_id=peer_id, fields=fields)
        )

    def messages_get_conversations(self, offset: int = 0, count: int = 20, filter: str = 'all', extended: int = None,
                                   start_message_id: int = None, fields: List[str] = None):
        """
        :param offset: Cмещение, необходимое для выборки определенного подмножества результатов.
        :param count: Максимальное число результатов, которые нужно получить.
        :param filter: Фильтр. Возможные значения: all, unread, important, unanswered.
        :param extended: Возвращать дополнительные поля.
        :param start_message_id: Идентификатор сообщения, начиная с которого нужно возвращать беседы.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetConversations(
            self.method(
                'messages.getConversations', group_id=self.group_id, offset=offset, count=count, filter=filter,
                extended=extended, start_message_id=start_message_id, fields=fields)
        )

    def messages_get_conversations_by_id(self, peer_ids: List[int], extended: int = None, fields: List[str] = None):
        """
        :param peer_ids: Идентификаторы назначений.
        :param extended: Возвращать дополнительные поля.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetConversationsById(
            self.method('messages.getConversationsById', group_id=self.group_id, peer_ids=peer_ids, extended=extended,
                        fields=fields)
        )

    def messages_get_history(self, offset: int = None, count: int = 20, user_id: int = None, peer_id: int = None,
                             start_message_id: int = None, rev: int = None, extended: int = None,
                             fields: List[str] = None):
        """
        :param offset: Cмещение, необходимое для выборки определенного подмножества сообщений
        :param count: Количество сообщений, которое необходимо получить (но не более 200)
        :param user_id: Идентификатор пользователя, историю переписки с которым необходимо вернуть.
        :param peer_id: Идентификатор назначения.
        :param start_message_id: Идентификатор сообщения, начиная с которого нужно возвращать беседы.
        :param rev: Возвращать сообщения в хронологическом порядке (по умолчанию).
        :param extended: Возвращать дополнительные поля.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetHistory(
            self.method(
                'messages.getHistory', group_id=self.group_id, offset=offset, count=count, user_id=user_id,
                peer_id=peer_id,
                start_message_id=start_message_id, rev=rev, extended=extended, fields=fields)
        )

    def messages_get_history_attachments(self, peer_id: int, media_type: List[str] = None, start_from: str = None,
                                         count: int = 20, photo_sizes: int = None, fields: List[str] = None,
                                         preserve_order: int = None, max_forwards_level: int = 45):
        """
        :param peer_id: Идентификатор назначения.
        :param media_type: Тип материалов, который необходимо вернуть.
        Доступные значения: photo, video, audio, doc, link, market, wall, share.

        :param start_from: Смещение, необходимое для выборки определенного подмножества объектов.
        :param count: Количество объектов, которое необходимо получить (но не более 200).
        :param photo_sizes: Параметр, указывающий нужно ли возвращать ли доступные размеры фотографии в специальном формате.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        :param preserve_order: Параметр, указывающий нужно ли возвращать вложения в оригинальном порядке.
        :param max_forwards_level: Максимальная глубина вложенности пересланных сообщений.
        """

        return MessagesGetHistoryAttachments(
            self.method(
                'messages.getHistoryAttachments', group_id=self.group_id, peer_id=peer_id, media_type=media_type,
                start_from=start_from, count=count, photo_sizes=photo_sizes, fields=fields,
                preserve_order=preserve_order, max_forwards_level=max_forwards_level)
        )

    def messages_get_important_messages(self, count: int = 20, offset: int = None, start_message_id: int = None,
                                        preview_length: int = None, fields: List[str] = None, extended: int = None):
        """
        :param count: Максимальное число результатов, которые нужно получить.
        :param offset: Смещение, необходимое для выборки определенного подмножества результатов.
        :param start_message_id: Идентификатор сообщения, начиная с которого нужно возвращать список.
        :param preview_length:
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        :param extended: Возвращать дополнительные поля.
        """

        return MessagesGetImportantMessages(
            self.method(
                'messages.getImportantMessages', group_id=self.group_id, count=count, offset=offset,
                start_message_id=start_message_id, preview_length=preview_length, fields=fields, extended=extended)
        )

    def messages_get_intent_users(self, intent: str, subscribe_id: int = None, offset: int = None, count: int = 20,
                                  extended: int = None, name_case: List[str] = None, fields: List[str] = None):
        """
        :param intent: Тип интента, который требует подписку.
        :param subscribe_id: ID подписки, необходимый для confirmed_notification.
        :param offset: Смещение, необходимое для выборки определенного подмножества.
        :param count: Количество подписчиков, информацию о которых необходимо получить.
        :param extended: Возвращать дополнительные поля.
        :param name_case: падеж для склонения имени и фамилии пользователя.
        Возможные значения:
        именительный – nom, родительный – gen, дательный – dat, винительный – acc,
        творительный – ins, предложный – abl. По умолчанию nom.

        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesGetIntentUsers(
            self.method(
                'messages.getIntentUsers', intent=intent, subscribe_id=subscribe_id, offset=offset, count=count,
                extended=extended, name_case=name_case, fields=fields)
        )

    def messages_get_invite_link(self, peer_id: int, reset: int = None):
        """
        :param peer_id: Идентификатор назначения.
        :param reset: Сгенерировать новую ссылку, сбросив предыдущую.
        """

        return MessagesGetInviteLink(
            self.method('messages.getInviteLink', group_id=self.group_id, peer_id=peer_id, reset=reset)
        )

    def messages_get_longpoll_history(self, ts: int, pts: int, preview_length: int = None, onlines: int = None,
                                      fields: List[str] = None, events_limit: int = 1000, msgs_limit: int = 200,
                                      max_msg_id: int = None, lp_version: int = 3, last_n: int = 0,
                                      credentials: int = None):
        """
        :param ts: Последнее значение параметра ts.
        :param pts: последнее значение параметра new_pts.
        :param preview_length: Количество символов, по которому нужно обрезать сообщение.
        :param onlines: Возвращать в числе прочих события 8 и 9 (пользователь стал онлайн/оффлайн).
        :param fields: Список дополнительных полей профилей, которые необходимо вернуть.
        :param events_limit: Лимит по количеству всех событий в истории.
        Обратите внимание, параметры events_limit и msgs_limit применяются совместно.
        Число результатов в ответе ограничивается первым достигнутым лимитом.

        :param msgs_limit: Лимит по количеству событий с сообщениями в истории.
        :param max_msg_id: Максимальный идентификатор сообщения среди уже имеющихся в локальной копии.
        :param lp_version: Версия Long Poll.
        :param last_n:
        :param credentials:
        """

        return MessagesGetLongpollHistory(
            self.method(
                'messages.getLongPollHistory', group_id=self.group_id, ts=ts, pts=pts,
                preview_length=preview_length, onlines=onlines, fields=fields, events_limit=events_limit,
                msgs_limit=msgs_limit, max_msg_id=max_msg_id, lp_version=lp_version,
                last_n=last_n, credentials=credentials)
        )

    def messages_get_longpoll_server(self, need_pts: int = None, lp_version: int = 3):
        """
        :param need_pts: Возвращать поле pts, необходимое для работы метода messages.getLongPollHistory.
        :param lp_version: Версия Long Poll.
        """
        return MessagesGetLongpollServer(
            self.method('messages.getLongPollServer', group_id=self.group_id, need_pts=need_pts, lp_version=lp_version)
        )

    def messages_is_messages_from_group_allowed(self, user_id: int):
        """
        :param user_id: Идентификатор пользователя.
        """
        return MessagesIsMessagesFromGroupAllowed(
            self.method('messages.isMessagesFromGroupAllowed', group_id=self.group_id, user_id=user_id)
        )

    def messages_mark_as_answered_conversation(self, peer_id: int, answered: int = 1):
        """
        :param peer_id: Идентификатор беседы.
        :param answered: Беседа отмечена отвеченной.
        """
        return self.method('messages.markAsAnsweredConversation', group_id=self.group_id, peer_id=peer_id,
                           answered=answered)

    def messages_mark_as_important_conversation(self, peer_id: int, important: int = 1):
        """
        :param peer_id: Идентификатор беседы
        :param important: Если сообщения необходимо пометить, как важные.
        """
        return self.method('messages.markAsImportantConversation', group_id=self.group_id, peer_id=peer_id,
                           important=important)

    def messages_mark_as_read(self, message_ids: List[int] = None, peer_id: str = None, start_message_id: int = None,
                              mark_conversation_as_read: int = None):
        """
        :param message_ids: Идентификаторы сообщений.
        :param peer_id: Идентификатор назначения.
        :param start_message_id: При передаче этого параметра будут помечены как прочитанные все сообщения, начиная с данного.
        :param mark_conversation_as_read:
        """

        return self.method('messages.markAsRead', group_id=self.group_id, message_ids=message_ids, peer_id=peer_id,
                           start_message_id=start_message_id, mark_conversation_as_read=mark_conversation_as_read)

    def messages_pin(self, peer_id: int, message_id: int, conversation_message_id: int):
        """
        :param peer_id: Идентификатор назначения.
        :param message_id: Идентификатор сообщения, которое нужно закрепить.
        :param conversation_message_id: Идентификатор сообщения беседы, которое нужно закрепить.
        """
        return MessagesPin(
            self.method('messages.pin', peer_id=peer_id, message_id=message_id,
                        conversation_message_id=conversation_message_id)
        )

    def messages_remove_chat_user(self, chat_id: int, user_id: int = None, member_id: int = None):
        """
        :param chat_id: Идентификатор беседы.
        :param user_id: Идентификатор пользователя, которого необходимо исключить из беседы.
        :param member_id: Идентификатор участника, которого необходимо исключить из беседы.
        Для сообществ — идентификатор сообщества со знаком «минус».
        """
        return self.method('messages.removeChatUser', chat_id=chat_id, user_id=user_id, member_id=member_id)

    def messages_restore(self, message_id: int):
        """
        :param message_id: Идентификатор сообщения, которое нужно восстановить.
        """
        return self.method('messages.restore', message_id=message_id)

    def messages_search(self, q: str = None, peer_id: int = None, date: int = None, preview_length: int = 0,
                        offset: int = None, count: int = 20, extended: int = None, fields: List[str] = None):
        """
        :param q: Подстрока, по которой будет производиться поиск.
        :param peer_id: Фильтр по идентификатору назначения для поиска по отдельному диалогу.
        :param date: Дата в формате DDMMYYYY.
         Если параметр задан, в ответе будут только сообщения, отправленные до указанной даты.
        :param preview_length: Количество символов, по которому нужно обрезать сообщение.
        :param offset: Смещение, необходимое для выборки определенного подмножества сообщений из списка найденных.
        :param count: Количество сообщений, которое необходимо получить.
        :param extended: Возвращать дополнительные поля для пользователей и сообществ.
        :param fields: Список ыудополнительных полей для пользователей и сообществ.
        """

        return MessagesSearch(
            self.method('messages.search', group_id=self.group_id, q=q, peer_id=peer_id, date=date,
                        preview_length=preview_length, offset=offset, count=count, extended=extended, fields=fields)
        )

    def messages_search_conversations(self, q: str, count: int = 20, extended: int = None, fields: List[str] = None):
        """
        :param q: Поисковой запрос.
        :param count: Максимальное число результатов для получения.
        :param extended: Возвращать дополнительные поля.
        :param fields: Дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        """

        return MessagesSearchConversations(
            self.method(
                'messages.searchConversations', group_id=self.group_id, q=q, count=count, extended=extended,
                fields=fields)
        )

    def messages_send(self, user_id: int = None, peer_id: int = None, peer_ids: List[int] = None, domain: str = None,
                      chat_id: int = None, message: str = None, lat: float = None, long: float = None, attachment=None,
                      reply_to: int = None, forward_messages: List[int] = None, forward=None, sticker_id: int = None,
                      keyboard=None, template: Dict = None, payload=None, content_source: Dict = None,
                      dont_parse_links: int = None, disable_mentions: int = None, intent: str = 'default',
                      subscribe_id: int = None):
        """
        :param user_id: Идентификатор пользователя, которому отправляется сообщение.
        :param peer_id: Идентификатор назначения.
        :param peer_ids: Идентификаторы получателей сообщения (при необходимости отправить сообщение сразу нескольким пользователям)
        :param domain: Короткий адрес пользователя.
        :param chat_id: Идентификатор беседы, к которой будет относиться сообщение.
        :param message: Текст личного сообщения. Обязательный параметр, если не задан параметр attachment.
        :param lat: Географическая широта (от -90 до 90).
        :param long: Географическая долгота (от -180 до 180).
        :param attachment: Медиавложения к личному сообщению, перечисленные через запятую.
        :param reply_to: Идентификатор сообщения, на которое требуется ответить.
        :param forward_messages: Идентификаторы пересылаемых сообщений.
        :param forward: JSON-объект.
        :param sticker_id: Идентификатор стикера.
        :param keyboard: Объект, описывающий клавиатуру бота.
        :param template: Объект, описывающий шаблон сообщения.
        :param payload: Полезная нагрузка.
        :param content_source: Объект, описывающий источник пользовательского контента для чат-ботов.
        :param dont_parse_links: Не создавать сниппет ссылки из сообщения.
        :param disable_mentions: Отключить уведомление об упоминании в сообщении.
        :param intent: Строка, описывающая интенты.
        :param subscribe_id:
        """

        return self.method('messages.send', group_id=self.group_id, user_id=user_id, peer_id=peer_id, peer_ids=peer_ids,
                           domain=domain, chat_id=chat_id, message=message, lat=lat, long=long, attachment=attachment,
                           reply_to=reply_to, forward_messages=forward_messages, forward=forward, sticker_id=sticker_id,
                           keyboard=keyboard, template=template, payload=payload, content_source=content_source,
                           dont_parse_links=dont_parse_links, disable_mentions=disable_mentions, intent=intent,
                           subscribe_id=subscribe_id, random_id=get_random_id())

    def messages_send_message_event_answer(self, event_id: str, user_id: int, peer_id: int, event_data=None):
        """
        :param event_id: Случайная строка, которая возвращается в событии message_event.
        :param user_id: Идентификатор пользователя.
        :param peer_id: Идентификатор диалога со стороны сообщества.
        :param event_data: Объект действия, которое должно произойти после нажатия на кнопку.
        """
        return self.method('messages.sendMessageEventAnswer', event_id=event_id, user_id=user_id, peer_id=peer_id,
                           event_data=event_data)

    def messages_set_activity(self, user_id: int, type: str, peer_id: int):
        """
        :param user_id: Идентификатор пользователя.

        :param type: typing — пользователь начал набирать текст,
                     audiomessage — пользователь записывает голосовое сообщение.

        :param peer_id: Идентификатор назначения.
        """
        return self.method('messages.setActivity', group_id=self.group_id, user_id=user_id, type=type, peer_id=peer_id)

    def messages_set_chat_photo(self, file: str):
        """
        :param file: Содержимое поля response из ответа специального upload сервера,
                     полученного в результате загрузки изображения на адрес,
                     полученный методом photos.getChatUploadServer.
        """
        return MessagesSetChatPhoto(self.method('messages.setChatPhoto', file=file))

    def messages_unpin(self, peer_id: int):
        """
        :param peer_id: Идентификатор назначения.
        """
        return self.method('messages.unpin', group_id=self.group_id, peer_id=peer_id)

    def groups_add_address(self, title: str, address: str, country_id: int, city_id: int, latitude: float,
                           longitude: float, metro_id: int = None, additional_address: str = None, phone: str = None,
                           work_info_status: str = None, timetable=None, is_main_address: int = None):
        """
        :param title: Заголовок адреса.
        :param address: Строка адреса.
        :param additional_address: Дополнительное описание адреса.
        :param country_id: Идентификатор страны.
        :param city_id: Идентификатор города.
        :param latitude: Географическая широта отметки, заданная в градусах (от -90 до 90).
        :param longitude: Географическая долгота отметки, заданная в градусах (от -180 до 180)
        :param metro_id: Идентификатор станции метро.
        :param phone: Номер телефона.

        :param work_info_status: тип расписания. Возможные значения:
                                 no_information -- нет информации о расписании;
                                 temporarily_closed — временно закрыто;
                                 always_opened — открыто круглосуточно;
                                 forever_closed — закрыто навсегда;
                                 timetable — открыто в указанные часы работы.
                                 Для этого типа расписания необходимо передать параметр timetable;

        :param timetable:
        :param is_main_address: Установить адрес основным.
        """
        return self.method('groups.addAddress', group_id=self.group_id, title=title, address=address,
                           country_id=country_id, city_id=city_id, latitude=latitude, longitude=longitude,
                           metro_id=metro_id, additional_address=additional_address, phone=phone,
                           work_info_status=work_info_status, timetable=timetable, is_main_address=is_main_address)

    def groups_delete_address(self, address_id: int):
        """
        :param address_id: Идентификатор адреса.
        """
        return self.method('groups.deleteAddress', group_id=self.group_id, address_id=address_id)

    def groups_disable_online(self):
        return self.method('groups.disableOnline', group_id=self.group_id)

    def groups_edit(self, title: str = None, description: str = None, screen_name: str = None,
                    access: int = None, website: str = None, subject: int = None, email: str = None,
                    phone: str = None, rss: str = None, event_start_date: int = None, event_finish_date: int = None,
                    event_group_id: int = None, public_category: int = None, public_subcategory: int = None,
                    public_date: str = None, wall: int = None, topics: int = None, photos: int = None,
                    video: int = None, audio: int = None, links: int = None, events: int = None, places: int = None,
                    contacts: int = None, docs: int = None, wiki: int = None, messages: int = None,
                    articles: int = None, addresses: int = None, age_limits: int = None, market: int = None,
                    market_comments: int = None, market_country: List[int] = None, market_city: List[int] = None,
                    market_currency: int = None, market_contact: int = None, market_wiki: int = None,
                    obscene_filter: int = None, obscene_stopwords: int = None, obscene_words: List[str] = None,
                    main_section: int = None, secondary_section: int = None, country: int = None, city: int = None):
        """
        :param title: Название сообщества.
        :param description: Описание сообщества.
        :param screen_name: Короткое имя сообщества.
        :param access: тип группы. Возможные значения:
                                   0 -- открытая;
                                   1 -- закрытая;
                                   2 -- частная;
        :param website: Адрес сайта, который будет указан в информации о группе.
        :param subject: Тематика сообщества.
        :param email: Электронный адрес организатора (для мероприятий).
        :param phone: Номер телефона организатора (для мероприятий).
        :param rss: Адрес rss для импорта новостей
        :param event_start_date: Дата начала события.
        :param event_finish_date: Дата окончания события.
        :param event_group_id: идентификатор группы, которая является организатором события (только для событий).
        :param public_category: Категория публичной страницы.
        :param public_subcategory: Подкатегория публичной станицы.
        :param public_date: дата основания компании, организации,
                            которой посвящена публичная страница в виде строки формата "dd.mm.YYYY".
        :param wall: Стена. Возможные значения:
                            0 — выключена;
                            1 — открытая;
                            2 — ограниченная (доступно только для групп и событий);
                            3 — закрытая (доступно только для групп и событий).
        :param topics: Обсуждения. Возможные значения:
                                   0 — выключены;
                                   1 — открытые;
                                   2 — ограниченные (доступно только для групп и событий).
        :param photos: Фотографии. Возможные значения:
                                   0 — выключены;
                                   1 — открытые;
                                   2 — ограниченные (доступно только для групп и событий).
        :param video: Видеозаписи. Возможные значения:
                                   0 — выключены;
                                   1 — открытые;
                                   2 — ограниченные (доступно только для групп и событий).
        :param audio: Аудиозаписи. Возможные значения:
                                   0 — выключены;
                                   1 — открытые;
                                   2 — ограниченные (доступно только для групп и событий).
        :param links: Ссылки (доступно только для публичных страниц).
                      Возможные значения:
                      0 — выключены;
                      1 — включены.
        :param events: События (доступно только для публичных страниц).
                       Возможные значения:
                       0 — выключены;
                       1 — включены.
        :param places: Места (доступно только для публичных страниц).
                       Возможные значения:
                       0 — выключены;
                       1 — включены.
        :param contacts: Контакты (доступно только для публичных страниц).
                         Возможные значения:
                         0 — выключены;
                         1 — включены.
        :param docs: Документы сообщества.
                     Возможные значения:
                     0 — выключены;
                     1 — открытые;
                     2 — ограниченные (доступно только для групп и событий).
        :param wiki: wiki-материалы сообщества.
                     Возможные значения:
                     0 — выключены;
                     1 — открытые;
                     2 — ограниченные (доступно только для групп и событий).
        :param messages: Сообщения сообщества.
                         Возможные значения:
                         0 — выключены;
                         1 — включены.
        :param articles:
        :param addresses:
        :param age_limits: Возрастное ограничение для сообщества.
                           Возможные значения:
                           1 — нет ограничений;
                           2 — 16+;
                           3 — 18+.
        :param market: Товары.
                       Возможные значения:
                       0 — выключены;
                       1 — включены.
        :param market_comments: Комментарии к товарам. Возможные значения:
                                0 — выключены;
                                1 — включены.
        :param market_country: Регионы доставки товаров.
        :param market_city: Города доставки товаров (в случае если указана одна страна).
        :param market_currency: Идентификатор валюты магазина.
                                Возможные значения:
                                643 — российский рубль;
                                980 — украинская гривна;
                                398 — казахстанский тенге;
                                978 — евро;
                                840 — доллар США.
        :param market_contact: Контакт для связи для продавцом.
        :param market_wiki: Идентификатор wiki-страницы с описанием магазина.
        :param obscene_filter: Фильтр нецензурных выражений в комментариях.
                               Возможные значения:
                               0 — выключен;
                               1 — включен.
        :param obscene_stopwords: Фильтр по ключевым словам в комментариях.
                                  Возможные значения:
                                  0 — выключен;
                                  1 — включен.
        :param obscene_words: Ключевые слова для фильтра комментариев.
        :param main_section:
        :param secondary_section:
        :param country:
        :param city:
        """

        return self.method('groups.edit', group_id=self.group_id, title=title, description=description,
                           screen_name=screen_name,
                           access=access, website=website, subject=subject, email=email, phone=phone, rss=rss,
                           event_start_date=event_start_date, event_finish_date=event_finish_date,
                           event_group_id=event_group_id,
                           public_category=public_category, public_subcategory=public_subcategory,
                           public_date=public_date,
                           wall=wall, topics=topics, photos=photos, video=video, audio=audio, links=links,
                           events=events,
                           places=places, contacts=contacts, docs=docs, wiki=wiki, messages=messages, articles=articles,
                           addresses=addresses, age_limits=age_limits, market=market, market_comments=market_comments,
                           market_country=market_country, market_city=market_city, market_currency=market_currency,
                           market_contact=market_contact, market_wiki=market_wiki, obscene_filter=obscene_filter,
                           obscene_stopwords=obscene_stopwords, obscene_words=obscene_words, main_section=main_section,
                           secondary_section=secondary_section, country=country, city=city)

    def groups_edit_address(self, address_id: int, title: str = None, address: str = None,
                            additional_address: str = None, country_id: int = None, city_id: int = None,
                            metro_id: int = None, latitude: float = None, longitude: float = None, phone: str = None,
                            work_info_status: str = None, timetable=None, is_main_address: int = None):
        """
        :param address_id: Идентификатор адреса.
        :param title: Заголовок адреса.
        :param address: Строка адреса. `Невский проспект, дом 28`
        :param additional_address: Дополнительное описание адреса.
        :param country_id: Идентификатор страны.
        :param city_id: Идентификатор города.
        :param metro_id: Идентификатор станции метро.
        :param latitude: Географическая широта отметки, заданная в градусах (от -90 до 90).
        :param longitude: Географическая долгота отметки, заданная в градусах (от -180 до 180).
        :param phone: Номер телефона.
        :param work_info_status: Тип расписания.
        :param timetable:
        :param is_main_address: Установить адрес основным.
        """
        return self.method('groups.editAddress', group_id=self.group_id, address_id=address_id, title=title,
                           address=address, additional_address=additional_address, country_id=country_id,
                           city_id=city_id, metro_id=metro_id, latitude=latitude, longitude=longitude, phone=phone,
                           work_info_status=work_info_status, timetable=timetable, is_main_address=is_main_address)

    def groups_enable_online(self):
        return self.method('groups.enableOnline', group_id=self.group_id)

    def groups_get_by_id(self, fields: List[str] = None):
        """
        :param fields: Список дополнительных полей, которые необходимо вернуть.
        """

        return GroupsGetById(self.method('groups.getById', group_id=self.group_id, fields=fields))

    def groups_get_members(self, sort: str = 'id_asc', offset: int = 0, count: int = 1000, fields: List[str] = None):
        """
        :param sort: Сортировка, с которой необходимо вернуть список участников.
                     Возможные значения:
                     id_asc — в порядке возрастания id;
                     id_desc — в порядке убывания id;
                     time_asc — в хронологическом порядке по вступлению в сообщество;
                     time_desc — в антихронологическом порядке по вступлению в сообщество.
        :param offset: Смещение, необходимое для выборки определенного подмножества участников.
        :param count: Количество участников сообщества, информацию о которых необходимо получить.
        :param fields: Список дополнительных полей, которые необходимо вернуть.
        """
        return GroupsGetMembers(
            self.method('groups.getMembers', group_id=self.group_id, sort=sort, offset=offset, fields=fields,
                        count=count)
        )

    def groups_is_member(self, user_id: int = None, user_ids: List[int] = None):
        """
        :param user_id: Идентификатор пользователя.
        :param user_ids: Идентификаторы пользователей, не более 500.
        """

        return GroupsIsMember(
            self.method('groups.isMember', group_id=self.group_id, user_id=user_id, user_ids=user_ids, extended=1)
        )

    def groups_get_banned(self, fields: List[str] = None, count: int = 20, owner_id: int = None, offset: int = None):
        """
        :param fields: Смещение, необходимое для выборки определенного подмножества черного списка.
        :param count: Количество пользователей, которое необходимо вернуть.
        :param owner_id: Идентификатор пользователя или сообщества из чёрного списка, информацию о котором нужно получить.
        :param offset: Смещение, необходимое для выборки определенного подмножества черного списка.
        """

        return GroupsGetBanned(
            self.method('groups.getBanned', group_id=self.group_id, offset=offset, count=count, fields=fields,
                        owner_id=owner_id)
        )

    def groups_get_online_status(self):
        return GroupsGetOnlineStatus(self.method('groups.getOnlineStatus', group_id=self.group_id))

    def groups_get_token_permissions(self):
        return GroupsGetTokenPermissions(self.method('groups.getTokenPermissions'))

    def groups_set_settings(self, messages: int = None, bots_capabilities: int = None, bots_start_button: int = None,
                            bots_add_to_chat: int = None):
        """
        :param messages: Сообщения сообщества.
                         Возможные значения:
                         0 — выключены;
                         1 — включены.
        :param bots_capabilities: Возможности ботов (использование клавиатуры, добавление в беседу).
                                  Возможные значения:
                                  0 — выключены;
                                  1 — включены.
        :param bots_start_button: Кнопка «Начать» в диалоге с сообществом. Работает, в случае если bots_capabilities=1.
                                  Возможные значения:
                                  0 — выключена;
                                  1 — включена.
        :param bots_add_to_chat: Добавление бота в беседы. Работает, в случае если bots_capabilities=1.
                                 Возможные значения:
                                 0 — запрещено;
                                 1 — разрешено.
        """
        return self.method('groups.setSettings', group_id=self.group_id, messages=messages,
                           bots_capabilities=bots_capabilities,
                           bots_start_button=bots_start_button, bots_add_to_chat=bots_add_to_chat)

    def groups_get_longpoll_server(self):
        return self.method('groups.getLongPollServer', group_id=self.group_id)

    def board_delete_comment(self, topic_id: int, comment_id: int):
        """
        :param topic_id: Идентификатор обсуждения.
        :param comment_id: Идентификатор комментария в обсуждении.
        """
        return self.method('board.deleteComment', group_id=self.group_id, topic_id=topic_id, comment_id=comment_id)

    def board_restore_comment(self, topic_id: int, comment_id: int):
        """
        :param topic_id: Идентификатор обсуждения.
        :param comment_id: Идентификатор комментария.
        """
        return self.method('board.restoreComment', group_id=self.group_id, topic_id=topic_id, comment_id=comment_id)

    def docs_get_messages_upload_server(self, peer_id: int, type: str = 'doc'):
        """
        :param peer_id: Идентификатор назначения.
        :param type: Тип документа.
                     Возможные значения:
                     doc — обычный документ;
                     audio_message — голосовое сообщение;
        """
        return DocsGetMessagesUploadServer(
            self.method('docs.getMessagesUploadServer', peer_id=peer_id, type=type)
        ).upload_url

    def docs_get_wall_upload_server(self):
        return DocsGetWallUploadServer(self.method('docs.getWallUploadServer', group_id=self.group_id))

    def docs_save(self, file, title: str = None, tags: List[str] = None, return_tags: int = None):
        """
        :param file: Параметр, возвращаемый в результате загрузки файла на сервер.
        :param title: Название документа.
        :param tags: Метки для поиска.
        :param return_tags:
        """

        return DocsSave(self.method('docs.save', file=file, title=title, tags=tags, return_tags=return_tags))

    def docs_search(self, q: str, search_own: int = None, count: int = 20, offset: int = None, return_tags: int = None):
        """
        :param q: Строка поискового запроса. Например, зеленые тапочки.
        :param search_own: 1 — искать среди собственных документов пользователя.
        :param count: Количество документов, информацию о которых нужно вернуть.
        :param offset: Смещение, необходимое для выборки определенного подмножества документов.
        :param return_tags:
        """
        return DocsSearch(
            self.method('docs.search', q=q, search_own=search_own, count=count, offset=offset, return_tags=return_tags))

    def market_edit_order(self, user_id: int, order_id: int, merchant_comment: str = None, status: int = None,
                          track_number: str = None, payment_status: str = None, delivery_price: int = None,
                          width: float = None, length: float = None, height: float = None, weight: float = None,
                          comment_for_user: str = None):
        """
        :param user_id: Идентификатор пользователя.
        :param order_id: Идентификатор заказа.
        :param merchant_comment: Комментарий продавца.
        :param status: Статус заказа.
                       Возможные значения:
                           0 - новый;
                           1 - согласуется;
                           2 - собирается;
                           3 - доставляется;
                           4 - выполнен;
                           5 - отменен;
                           6 - возвращен.
        :param track_number: Трек-номер.
        :param payment_status: Статус платежа.
                               Возможные значения:
                                   not_paid - не оплачен;
                                   paid - оплачен;
                                   returned - возвращен.
        :param delivery_price: Стоимость доставки.
        :param width: Ширина.
        :param length: Длина.
        :param height: Высота.
        :param weight: Вес.
        :param comment_for_user:
        """
        return self.method('market.editOrder', user_id=user_id, order_id=order_id, merchant_comment=merchant_comment,
                           status=status, track_number=track_number, payment_status=payment_status,
                           delivery_price=delivery_price,
                           width=width, length=length, height=height, weight=weight, comment_for_user=comment_for_user)

    def market_get_group_orders(self, offset: int = None, count: int = 10):
        """
        :param offset: Смещение относительно первого найденного заказа для выборки определенного подмножества.
        :param count: Количество возвращаемых заказов.
        """
        return MarketGetGroupOrders(
            self.method('market.getGroupOrders', group_id=self.group_id, offset=offset, count=count)
        )

    def market_get_order_by_id(self, order_id: int, user_id: int = None, extended: int = None):
        """
        :param order_id: Идентификатор заказа.
        :param user_id: Идентификатор пользователя.
        :param extended:
        """
        return self.method('market.getOrderById', user_id=user_id, order_id=order_id, extended=extended)

    def market_get_order_items(self, order_id: int, user_id: int = None, offset: int = None, count: int = 50):
        """
        :param order_id: Идентификатор заказа.
        :param user_id: Id пользователя, который сделал заказ.
        :param offset: Смещение относительно первого найденного товара в заказе для выборки определенного подмножества.
        :param count: Количество возвращаемых товаров в заказе.
        """
        return MarketGetOrderItems(
            self.method('market.getOrderItems', order_id=order_id, user_id=user_id, offset=offset, count=count)
        )

    def photos_get_chat_upload_server(self, chat_id: int, crop_x: float = None,
                                      crop_y: float = None, crop_width: int = None):
        """
        :param chat_id: Идентификатор беседы, для которой нужно загрузить фотографию.
        :param crop_x: Координата x для обрезки фотографии (верхний правый угол).
        :param crop_y: Координата y для обрезки фотографии (верхний правый угол).
        :param crop_width: Ширина фотографии после обрезки в px.
        """
        return PhotosGetChatUploadServer(
            self.method(
                'photos.getChatUploadServer', chat_id=chat_id, crop_x=crop_x, crop_y=crop_y, crop_width=crop_width
            )
        ).upload_url

    def photos_get_messages_upload_server(self):
        return PhotosGetMessagesUploadServer(self.method('photos.getMessagesUploadServer', peer_id=0))

    def photos_get_owner_cover_photo_upload_server(self, crop_x: float = None, crop_y: float = None,
                                                   crop_x2: float = None, crop_y2: float = None):
        """
        :param crop_x: Координата X верхнего левого угла для обрезки изображения.
        :param crop_y: Координата Y верхнего левого угла для обрезки изображения.
        :param crop_x2: Координата X нижнего правого угла для обрезки изображения.
        :param crop_y2: Координата Y нижнего правого угла для обрезки изображения.
        """
        return PhotosGetOwnerCoverPhotoUploadServer(
            self.method('photos.getOwnerCoverPhotoUploadServer', group_id=self.group_id, crop_x=crop_x, crop_y=crop_y,
                        crop_x2=crop_x2, crop_y2=crop_y2)).upload_url

    def photos_save_messages_photo(self, photo: str, server: int = None, hash: str = None):
        """
        :param photo: Параметр, возвращаемый в результате загрузки фотографии на сервер.
        :param server: Параметр, возвращаемый в результате загрузки фотографии на сервер.
        :param hash: Параметр, возвращаемый в результате загрузки фотографии на сервер.
        """
        return PhotosSaveMessagesPhoto(self.method('photos.saveMessagesPhoto', photo=photo, server=server, hash=hash))

    def photos_save_owner_cover_photo(self, hash: str, photo: str):
        """
        :param hash: Параметр hash, полученный в результате загрузки фотографии на сервер.
        :param photo: Параметр photo, полученный в результате загрузки фотографии на сервер.
        """
        return PhotosSaveOwnerCoverPhoto(self.method('photos.saveOwnerCoverPhoto', hash=hash, photo=photo))

    def podcasts_search_podcast(self, search_string: str, offset: int = None, count: int = 20):
        """
        :param search_string:
        :param offset:
        :param count:
        """
        return PodcastsSearchPodcast(
            self.method('podcasts.searchPodcast', search_string=search_string, offset=offset, count=count)
        )

    def storage_get(self, key: str = None, keys: List[str] = None, user_id: int = None):
        """
        :param key: Название переменной.
        :param keys: Список названий переменных. Если указано, параметр key не учитывается.
        :param user_id: id пользователя, переменная которого устанавливается, в случае если данные запрашиваются серверным методом.
        """

        return self.method('storage.get', key=key, keys=keys, user_id=user_id)

    def storage_get_keys(self, user_id: int, offset: int = None, count: int = 100) -> List:
        """
        :param user_id: id пользователя, названия переменных которого получаются, в случае если данные запрашиваются серверным методом.
        :param offset: Смещение, необходимое для выборки определенного подмножества названий переменных
        :param count: Количество названий переменных, информацию о которых необходимо получить.
        """
        return self.method('storage.getKeys', user_id=user_id, offset=offset, count=count)

    def storage_set(self, key: str, value: str = None, user_id: int = None):
        """
        :param key: Название переменной.
                    Может содержать символы латинского алфавита, цифры, знак тире, нижнее подчёркивание [a-zA-Z_\-0-9].
        :param value: Значение переменной, сохраняются только первые 4096 байта.
        :param user_id: id пользователя, переменная которого устанавливается, в случае если данные запрашиваются серверным методом.
        """
        return self.method('storage.set', key=key, value=value, user_id=user_id)

    def users_get(self, user_ids: List[int], fields: List[str] = None, name_case: str = 'nom'):
        """
        :param user_ids: Идентификаторы пользователей
        :param fields: Список дополнительных полей профилей, которые необходимо вернуть.
        :param name_case: Падеж для склонения имени и фамилии пользователя.
                          Возможные значения:
                              Именительный – nom,
                              Родительный – gen,
                              Дательный – dat,
                              Винительный – acc,
                              Творительный – ins,
                              Предложный – abl.
        """

        return self.method('users.get', user_ids=user_ids, fields=fields, name_case=name_case)

    def stories_delete(self, owner_id: int, story_id: int, stories: List[str] = None):
        """
        :param owner_id: Идентификатор владельца истории.
        :param story_id: Идентификатор истории.
        :param stories:
        """

        return self.method('stories.delete', owner_id=owner_id, story_id=story_id, stories=stories)

    def stories_get(self, owner_id: int, extended: int = None, fields: List[str] = None):
        """
        :param owner_id: Идентификатор пользователя, истории которого необходимо получить.
        :param extended: 1 — возвращать в ответе дополнительную информацию о профилях пользователей.
        :param fields:
        """

        return StoriesGet(self.method('stories.get', owner_id=owner_id, extended=extended, fields=fields))

    def stories_get_by_id(self, stories: List[int], extended: int = None, fields: List[str] = None):
        """
        :param stories: Идентификаторы историй.
        :param extended: 1 — возвращать в ответе дополнительную информацию о пользователях.
        :param fields: Дополнительные поля профилей и сообществ, которые необходимо вернуть в ответе.
        """

        return StoriesGetById(self.method('stories.getById', stories=stories, extended=extended, fields=fields))

    def stories_get_photo_upload_server(self, add_to_news: int = None, user_ids: List[int] = None,
                                        reply_to_story: str = None, link_text: str = None, link_url: str = None,
                                        clickable_stickers=None):
        """
        :param add_to_news: 1 — разместить историю в новостях. Обязательно, если не указан user_ids.
        :param user_ids: Идентификаторы пользователей, которые будут видеть историю (для отправки в личном сообщении).
                         Обязательно, если add_to_news не передан.
        :param reply_to_story: Идентификатор истории, в ответ на которую создается новая.
        :param link_text: Текст ссылки для перехода из истории.
        :param link_url: Адрес ссылки для перехода из истории. Допустимы только внутренние ссылки https://vk.com.
        :param clickable_stickers: Объект кликабельного стикера.
        """

        return StoriesGetPhotoUploadServer(
            self.method(
                'stories.getPhotoUploadServer', add_to_news=add_to_news, user_ids=user_ids,
                reply_to_story=reply_to_story, link_text=link_text, link_url=link_url,
                clickable_stickers=clickable_stickers)
        ).upload_result

    def stories_get_replies(self, owner_id: int, story_id: int, access_key: str = None,
                            extended: int = None, fields: List[str] = None):
        """
        :param owner_id: Идентификатор владельца истории.
        :param story_id: Идентификатор истории.
        :param access_key: Ключ доступа для приватного объекта.
        :param extended: 1 — возвращать дополнительную информацию о профилях и сообществах.
        :param fields: Дополнительные поля профилей и сообществ, которые необходимо вернуть в ответе.
        """

        return StoriesGetReplies(self.method('stories.getReplies', owner_id=owner_id, story_id=story_id,
                                             access_key=access_key, extended=extended, fields=fields))

    def stories_get_stats(self, owner_id: int, story_id: int):
        """
        :param owner_id: Идентификатор владельца истории.
        :param story_id: Идентификатор истории.
        """
        return StoriesGetStats(self.method('stories.getStats', owner_id=owner_id, story_id=story_id))

    def stories_get_video_upload_server(self, user_ids: List[int] = None, add_to_news: int = None,
                                        reply_to_story: str = None, link_text: str = None, link_url: str = None,
                                        clickable_stickers=None):
        """
        :param user_ids: Идентификаторы пользователей, которые будут видеть историю (для отправки в личном сообщении).
        :param add_to_news: 1 — разместить историю в новостях.
        :param reply_to_story: Идентификатор истории, в ответ на которую создается новая.
        :param link_text: Текст ссылки для перехода из истории.
        :param link_url: Адрес ссылки для перехода из истории.
        :param clickable_stickers: Объект кликабельного стикера.
        """
        user_ids = ','.join(str(el) for el in user_ids)

        return StoriesGetVideoUploadServer(
            self.method('stories.getVideoUploadServer', group_id=self.group_id, user_ids=user_ids,
                        add_to_news=add_to_news, reply_to_story=reply_to_story, link_text=link_text,
                        link_url=link_url, clickable_stickers=clickable_stickers)
        ).upload_result

    def stories_get_viewers(self, owner_id: int, story_id: int, count: int = 100,
                            offset: int = None, extended: int = None):
        """
        :param owner_id: Идентификатор владельца истории.
        :param story_id: Идентификатор истории.
        :param count: Максимальное число результатов в ответе.
        :param offset: Сдвиг для получения определённого подмножества результатов.
        :param extended: 1 — возвращать в ответе расширенную информацию о пользователях.
        """
        return StoriesGetViewers(
            self.method('stories.getViewers', owner_id=owner_id, story_id=story_id,
                        count=count, offset=offset, extended=extended)
        )

    def stories_hide_all_replies(self, owner_id: int):
        """
        :param owner_id: Идентификатор пользователя, ответы от которого нужно скрыть.
        """
        return self.method('stories.hideAllReplies', group_id=self.group_id, owner_id=owner_id)

    def stories_hide_reply(self, owner_id: int, story_id: int):
        """
        :param owner_id: Идентификатор владельца истории (ответной).
        :param story_id: Идентификатор истории (ответной).
        """
        return self.method('stories.hideReply', owner_id=owner_id, story_id=story_id)

    def stories_save(self, upload_results: List[str], extended: int = None, fields: List[str] = None):
        """
        :param upload_results: Cписок строк, которые возвращает stories.getPhotoUploadServer или stories.getVideoUploadServer.
        :param extended:
        :param fields:
        """

        return StoriesSave(self.method('stories.save', upload_results=upload_results, fields=fields, extended=extended))

    def utils_check_link(self, url: str):
        """
        :param url: Внешняя ссылка, которую необходимо проверить.
        """
        return UtilsCheckLink(self.method('utils.checkLink', url=url))

    def utils_get_link_stats(self, key: str, source: str = 'vk_cc', access_key: str = None, interval: str = 'day',
                             intervals_count: int = 1, extended: int = None):
        """
        :param key: Сокращенная ссылка (часть URL после "vk.cc/").
        :param source:
        :param access_key: Ключ доступа к приватной статистике ссылки.
        :param interval: Единица времени для подсчета статистики. Возможные значения: hour, day, week, month, forever.
        :param intervals_count: Длительность периода для получения статистики в выбранных единицах (из параметра interval).
        :param extended: 1 — возвращать расширенную статистику (пол/возраст/страна/город),
                         0 — возвращать только количество переходов.
        """
        return UtilsGetLinkStats(
            self.method('utils.getLinkStats', key=key, source=source, access_key=access_key,
                        interval=interval, intervals_count=intervals_count, extended=extended))

    def utils_get_server_time(self):
        """Возвращает число, соответствующее времени в UnixTime."""
        return self.method('utils.getServerTime')

    def utils_get_short_link(self, url: str, private: int = None):
        """
        :param url: URL, для которого необходимо получить сокращенный вариант.
        :param private: 1 — статистика ссылки приватная,
                        0 — статистика ссылки общедоступная.
        """
        return UtilsGetShortLink(self.method('utils.getShortLink', url=url, private=private))

    def utils_resolve_screen_name(self, screen_name: str):
        """
        :param screen_name: Короткое имя пользователя, группы или приложения.
        """
        return UtilsResolveScreenName(self.method('utils.resolveScreenName', screen_name=screen_name))

    def wall_close_comments(self, owner_id: int, post_id: int):
        return self.method('wall.closeComments', owner_id=owner_id, post_id=post_id)

    def wall_create_comment(self, post_id: int, message: str = None, reply_to_comment: int = None,
                            attachments=None, sticker_id: int = None):
        """
        :param post_id: Идентификатор записи на стене.
        :param message: Текст комментария. Обязательный параметр, если не передан параметр attachments.
        :param reply_to_comment: Идентификатор комментария, в ответ на который должен быть добавлен новый комментарий.
        :param attachments:
        :param sticker_id: Идентификатор стикера.
        """
        return WallCreateComment(
            self.method('wall.createComment', owner_id=-self.group_id, from_group=self.group_id,
                        guid=get_random_id(), post_id=post_id, message=message, reply_to_comment=reply_to_comment,
                        attachments=attachments, sticker_id=sticker_id))

