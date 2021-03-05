from .vk_types import *


class ResponseItem:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<Item({", ".join(f"{k}={v}" for k, v in self.__dict__.items())})>'


class Response:
    # TODO: Добавить итерацию или не надо ?
    def __init__(self, response):
        if isinstance(response, dict):
            self.__response = ResponseItem(**response)
            self.__dict__.update(self.__response.__dict__)
        else:
            self.__response = [ResponseItem(**el) for el in response]

    def __getitem__(self, i: int):
        return self.__response[i]

    def __repr__(self):
        if not isinstance(self.__response, list):
            return self.__response.__repr__()
        return "[{}]".format(',\n '.join(str(el) for el in self.__response))


class GroupsGetBanned(Response):
    count: int
    items: List[Dict]


class GroupsGetById(Response, Group):
    def __init__(self, *args):
        super().__init__(args[0])


class GroupsGetMembers(Response):
    count: int
    items: List[int]


class GroupsIsMember(Response):
    member: int
    request: int
    invitation: int
    can_invite: int
    can_recall: int
    user_id: int


class GroupsGetOnlineStatus(Response):
    status: str
    minutes: int


class GroupsGetTokenPermissions(Response):
    mask: int
    settings: List[Dict]


class DocsGetMessagesUploadServer(Response):
    upload_url: str


class DocsGetWallUploadServer(Response):
    upload_url: str


class DocsSearch(Response):
    count: int
    items: List[Dict]


class DocsSave(Response, Document):
    pass

class MessagesDeleteChatPhoto(Response):
    message_id: int
    chat: dict


class MessagesDeleteConversation(Response):
    last_deleted_id: int


class MessagesGetConversationMembers(Response):
    count: int
    items: List[Dict]
    profiles: List[Profile]
    groups: List[Group]


class MessagesGetByConversationMessageId(Response):
    count: int
    items: List[Dict]


class MessagesGetById(Response):
    count: int
    items: List[Dict]


class MessagesGetConversations(Response):
    count: int
    items: List[Dict]
    unread_count: int
    profiles: List[Profile]
    groups: List[Group]


class MessagesGetConversationsById(Response):
    count: int
    items: List[Dict]


class MessagesGetHistory(Response):
    count: int
    items: Dict
    in_read: int
    out_read: int


class MessagesGetHistoryAttachments(Response):
    items: List[Dict]
    next_from: str


class MessagesGetImportantMessages(Response):
    messages: Dict


class MessagesGetIntentUsers(Response):
    count: int
    items: List[int]


class MessagesGetInviteLink(Response):
    link: str


class MessagesIsMessagesFromGroupAllowed(Response):
    is_allowed: int


class MessagesPin(Response):
    id: int
    date: int
    from_id: int
    text: str
    attachments: List[Dict]
    geo: Dict
    fwd_messages: List[Dict]


class MessagesSearch(Response):
    count: int
    items: List[Dict]


class MessagesSearchConversations(Response):
    count: int
    items: List[Dict]


class MessagesSetChatPhoto(Response):
    message_id: int
    chat: Dict


class MessagesGetLongpollServer(Response):
    key: str
    server: str
    ts: int


class MessagesGetLongpollHistory(Response):
    history: List
    messages: List
    groups: List[Group]
    profiles: List[Profile]

class MarketGetGroupOrders(Response):
    count: int
    items: List[Dict]


class MarketGetOrderItems(Response):
    count: int
    items: List[Dict]


class PhotosGetChatUploadServer(Response):
    upload_url: str


class PhotosGetMessagesUploadServer(Response):
    upload_url: str
    album_id: int
    group_id: int


class PhotosGetOwnerCoverPhotoUploadServer(Response):
    upload_url: str


class PhotosSaveMessagesPhoto(Response):
    id: int
    pid: int
    aid: int
    owner_id: int
    src: str
    src_big: str
    src_small: str
    created: str
    src_xbig: str
    src_xxbig: str


class PhotosSaveOwnerCoverPhoto(Response):
    images: List[Dict]

class PodcastsSearchPodcast(Response):
    results_total: int
    podcasts: List[Dict]


class StoriesGet(Response):
    count: int
    items: List[Dict]
    profiles: List[Dict]
    groups: List[Dict]


class StoriesGetById(Response):
    count: int
    items: List[Dict]
    profiles: List[Dict]
    groups: List[Dict]


class StoriesGetPhotoUploadServer(Response):
    upload_result: str


class StoriesGetReplies(Response):
    count: int
    items: List[Dict]
    profiles: List[Dict]
    groups: List[Dict]


class StoriesGetStats(Response):
    views: Dict
    replies: Dict
    answer: Dict
    shares: Dict
    subscribers: Dict
    bans: Dict
    open_link: Dict


class StoriesGetVideoUploadServer(Response):
    upload_result: str


class StoriesGetViewers(Response):
    count: int
    items: List[Dict]


class StoriesSave(Response):
    count: int
    items: List[Dict]


class UtilsCheckLink(Response):
    status: str
    link: str


class UtilsGetLinkStats(Response):
    key: str
    stats: List[Dict]


class UtilsGetShortLink(Response):
    short_url: str
    access_key: str
    key: str
    url: str


class UtilsResolveScreenName(Response):
    type: str
    object_id: int


class WallCreateComment(Response):
    comment_id: int
    parent_stack: List[int]
