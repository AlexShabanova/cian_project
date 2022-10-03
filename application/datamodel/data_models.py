import enum


class DealType(enum.Enum):
    sale = 'sale'
    rent = 'rent'


class OfferType(enum.Enum):
    flat = 'flat'
    suburban = 'suburban'  # дом
    offices = 'offices'


class ObjectType(enum.Enum):
    # В параметр запроса object_type%5B0%5D
    new_build = 2
    secondary_build = 1


class RoomType(enum.Enum):
    # Возможные варианты 1 - 5 (количество комнат), 6 - многокомнатные, 7 - свободная планировка, 9 - студия
    room1 = 1
    room2 = 2
    room3 = 3
    room4 = 4
    room5 = 5
    room6 = 6
    room7 = 7
    room9 = 9


class Region(enum.Enum):
    moscow = 1
    st_petersburg = 2
