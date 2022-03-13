import enum
from typing import Any


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


class Result:
    pass


class Success(Result):
    def __init__(self, data: Any):
        self.data = data


class Error(Result):
    def __init__(self, exception: Exception):
        self.exception = exception

