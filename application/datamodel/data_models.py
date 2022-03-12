import enum


class DealType(enum.Enum):
    sale = 'sale'
    rent = 'rent'


class OfferType(enum.Enum):
    flat = 'flat'
    suburban = 'suburban'  # дом
    offices = 'offices'


class Region(enum.Enum):
    moscow = 1
    st_petersburg = 2