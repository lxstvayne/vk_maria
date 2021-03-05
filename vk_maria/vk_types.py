from typing import *


class Adresses(TypedDict):
    is_enabled: bool
    main_address_id: int


class BanInfo(TypedDict):
    end_date: int
    comment: str


class City(TypedDict):
    id: int
    title: str


class Contacts(TypedDict):
    user_id: int
    desc: str
    phone: str
    email: str


class Counters(TypedDict):
    pass


class Country(TypedDict):
    id: int
    title: str


class Images(TypedDict):
    url: str
    width: int
    height: int


class Cover(TypedDict):
    enabled: int
    images: List[Images]


class Links(TypedDict):
    id: int
    url: str
    name: str
    desc: str
    photo_50: str
    photo_100: str


class Currency(TypedDict):
    id: int
    name: str


class Market(TypedDict):
    enabled: int
    type: str
    price_min: int
    price_max: int
    main_album_id: int
    contact_id: int
    currency: Currency
    currency_text: str


class Place(TypedDict):
    id: int
    title: str
    latitude: float
    longitude: float
    type: str
    country: int
    city: int
    address: str


class Group:
    id: int
    name: str
    screen_name: str
    is_closed: int
    deactivated: str
    is_admin: int
    admin_level: int
    is_member: int
    is_advertiser: int
    invited_by: int
    type: str
    photo_50: str
    photo_100: str
    photo_200: str
    activity: str = None
    addresses: Adresses = None
    age_limits: int = None
    ban_info: BanInfo = None
    can_create_topic: int = None
    can_message: int = None
    can_post: int = None
    can_see_all_posts: int = None
    can_upload_doc: int = None
    can_upload_video: int = None
    city: City = None
    contacts: Contacts = None
    counters: Counters = None
    country: Country = None
    cover: Cover = None
    crop_photo: Dict = None
    description: str = None
    fixed_post: int = None
    has_photo: int = None
    is_favorite: int = None
    is_hidden_from_feed: int = None
    is_messages_blocked: int = None
    links: Links = None
    main_album_id: int = None
    main_section: int = None
    market: Market = None
    member_status: int = None
    members_count: int = None
    place: Place = None
    public_date_label: str = None
    site: str = None
    start_date: int = None
    finish_date: int = None
    status: str = None
    trending: int = None
    verified: int = None
    wall: int = None
    wiki_page: str = None


class Career(TypedDict):
    group_id: int
    company: str
    country_id: int
    city_id: int
    city_name: str
    from_: int
    until: int
    position: str


class City(TypedDict):
    id: int
    title: str


class Contacts(TypedDict):
    mobile_phone: str
    home_phone: str


class Counters(TypedDict):
    albums: int
    videos: int
    audios: int
    photos: int
    notes: int
    friends: int
    groups: int
    online_friends: int
    mutual_friends: int
    user_videos: int
    followers: int
    pages: int


class Country(TypedDict):
    id: int
    title: str


class Education(TypedDict):
    university: int
    university_name: str
    faculty: int
    faculty_name: str
    graduation: int


class LastSeen(TypedDict):
    time: int
    platform: int


class Military(TypedDict):
    unit: str
    unit_id: int
    country_id: int
    from_: int
    until: int


class Occupation(TypedDict):
    type: str
    id: int
    name: str


class Personal(TypedDict):
    political: int
    langs: List[str]
    religion: str
    inspired_by: str
    people_main: int
    life_main: int
    smoking: int
    alcohol: int


class Relatives(TypedDict):
    id: int
    name: str
    type: str


class Schools(TypedDict):
    id: int
    country: int
    city: int
    name: str
    year_from: int
    year_to: int
    year_graduated: int
    class_: str
    speciality: str
    type: int
    type_str: str


class Universities(TypedDict):
    id: int
    country: int
    city: int
    name: str
    faculty: int
    faculty_name: str
    chair: int
    chair_name: str
    graduation: int
    education_form: str
    education_status: str


class Profile:
    id: int
    first_name: str
    last_name: str
    deactivated: str
    is_closed: bool
    can_access_closed: bool
    about: str = None
    activities: str = None
    bdate: str = None
    blacklisted: int = None
    blacklisted_by_me: int = None
    books: str = None
    can_post: int = None
    can_see_all_posts: int = None
    can_see_audio: int = None
    can_send_friend_request: int = None
    can_write_private_message: int = None
    career: Career = None
    city: City = None
    common_count: int = None
    connections: str = None
    contacts: Contacts = None
    counters: Counters = None
    country: Country = None
    crop_photo: dict = None
    domain: str = None
    education: Education = None
    exports = None
    first_name_nom: str = None
    first_name_gen: str = None
    first_name_dat: str = None
    first_name_acc: str = None
    first_name_ins: str = None
    first_name_abl: str = None
    followers_count: int = None
    friend_status: int = None
    games: str = None
    has_mobile: int = None
    has_photo: int = None
    home_town: str = None
    interests: str = None
    is_favorite: int = None
    is_friend: int = None
    is_hidden_from_feed: int = None
    last_name_nom: str = None
    last_name_gen: str = None
    last_name_dat: str = None
    last_name_acc: str = None
    last_name_ins: str = None
    last_name_abl: str = None
    last_seen: LastSeen = None
    lists: str = None
    maiden_name: str = None
    military: Military = None
    movies: str = None
    music: str = None
    nickname: str = None
    occupation: Occupation = None
    online: int = None
    personal: Personal = None
    photo_50: str = None
    photo_100: str = None
    photo_200_orig: str = None
    photo_200: str = None
    photo_400_orig: str = None
    photo_id: str = None
    photo_max: str = None
    photo_max_orig: str = None
    quotes: str = None
    relatives: Relatives = None
    relation: int = None
    schools: Schools = None
    screen_name: str = None
    sex: int = None
    site: str = None
    status: str = None
    timezone: int = None
    trending: int = None
    tv: str = None
    universities: Universities = None
    verified: int = None
    wall_default: str = None


class BanInfo:
    admin_id: int
    date: int
    reason: int
    comment: str
    end_date: int


class Order:
    id: int
    group_id: int
    user_id: int
    date: int
    variants_grouping_id: int
    is_main_variant: bool
    property_values: List
    cart_quantity: int
    status: int
    items_count: int
    total_price: Dict
    display_order_id: str
    comment: str
    preview_order_items: List
    delivery: Dict
    recipient: Dict


class Document:
    id: int
    owner_id: int
    title: str
    size: int
    ext: str
    url: str
    date: int
    type: int
    preview: Dict
