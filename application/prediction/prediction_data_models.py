from enum import Enum


class FlatType(Enum):
    flat = 'квартира'
    apartaments = 'апартаменты'


class Rooms(Enum):
    studio = 0  # квартира-студия
    open_plan = -1  # свободная планировка
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6


class SaleType(Enum):
    free_sale = 'свободная продажа'
    alternative_sale = 'альтернатива'
    co_funding = 'долевое участие (214-фз)'


class Mortgage(Enum):
    mortgage_true = 1
    mortgage_false = 0


class BuiltYear(object):

    def __init__(self) -> None:
        self.__year = None

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year: int):
        if year < 1700:
            self.__year = 1700
        else:
            self.__year = year
    # 'пропущено'


class District(Enum):
    ZelAO = 'ЗелАО'
    TAO = 'ТАО (Троицкий)'
    SAO = 'САО'
    YAO = 'ЮАО'
    YVAO = 'ЮВАО'
    ZAO = 'ЗАО'
    SVAO = 'СВАО'
    VAO = 'ВАО'
    YZAO = 'ЮЗАО'
    SZAO = 'СЗАО'
    CAO = 'ЦАО'


class Seller(Enum):
    agency = 'агентство'
    realtor = 'частный риелтор'
    developer = 'застройщик'
    consultant = 'консультант'
    owner = 'собственник'
    not_mentioned = 'не указано'
    # 'пропущено'


class HousingType(Enum):
    second_built = 'вторичное'
    new_built = 'новостройка'
    missing = 'пропущено'
    # 'пропущено'


class CeilingHeight:
    def __init__(self) -> None:
        self.__height = None

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height: int):
        if 25 <= height <= 40:
            self.__height = round(height / 10, 2)
        elif height < 2.4 or 12 < height < 25:
            self.__height = None
        elif height < 240:
            self.__height = round(height / 100, 2)
        else:
            self.__height = height
    # 'пропущено'


class Bathroom(Enum):
    combined_1_wc = '1 совмещенный'
    separate_1_wc = '1 раздельный'
    combined_1_separate_1_wc = '1 совмещенный, 1 раздельный'
    combined_1_separate_2_wc = '1 совмещенный, 2 раздельных'
    combined_1_separate_3_wc = '1 совмещенный, 3 раздельных'
    combined_1_separate_4_wc = '1 совмещенный, 4 раздельных'
    combined_2_wc = '2 совмещенных'
    separate_2_wc = '2 раздельных'
    combined_2_separate_1_wc = '2 совмещенных, 1 раздельный'
    combined_2_separate_2_wc = '2 совмещенных, 2 раздельных'
    combined_2_separate_3_wc = '2 совмещенных, 3 раздельных'
    combined_2_separate_4_wc = '2 совмещенных, 4 раздельных'
    combined_3_wc = '3 совмещенных'
    separate_3_wc = '3 раздельных'
    combined_3_separate_1_wc = '3 совмещенных, 1 раздельный'
    combined_3_separate_2_wc = '3 совмещенных, 2 раздельных'
    combined_3_separate_3_wc = '3 совмещенных, 3 раздельных'
    combined_3_separate_4_wc = '3 совмещенных, 4 раздельных'
    combined_4_wc = '4 совмещенных'
    separate_4_wc = '4 раздельных'
    combined_4_separate_1_wc = '4 совмещенных, 1 раздельный'
    combined_4_separate_2_wc = '4 совмещенных, 2 раздельных'
    combined_4_separate_3_wc = '4 совмещенных, 3 раздельных'
    combined_4_separate_4_wc = '4 совмещенных, 4 раздельных'
    missing = 'пропущено'


class HouseType(Enum):
    brick = 'кирпичный'
    block = 'блочный'
    monolith_brick = 'монолитно-кирпичный'
    panel = 'панельный'
    monolith = 'монолитный'
    panel_monolith = 'панельный, монолитный'
    panel_brick = 'панельный, кирпичный'
    missing = 'пропущено'


class Parking(Enum):
    spontaneous = 'стихийная'
    above_ground = 'наземная'
    underground = 'подземная'
    guest = 'гостевая'
    outdoor = 'открытая'
    multilevel = 'многоуровневая'
    roof = 'на крыше'
    separate_multilevel = 'отдельная многоуровневая'
    underground_guest = 'подземная, гостевая'
    underground_separate_multilevel = 'подземная, отдельная многоуровневая'
    separate_multilevel_guest = 'отдельная многоуровневая, гостевая'
    underground_separate_multilevel_guest = 'подземная, отдельная многоуровневая, гостевая'


class Heating(Enum):
    centralized = 'центральное'
    boiler = 'котел/квартирное отопление'
    individual_heating_unit = 'индивидуальный тепловой пункт'
    independent_boiling_room = 'автономная котельная'


class SuspiciousFlat(Enum):
    suspicious = 1
    not_suspicious = 0


class InteriorDesign(Enum):
    cosmetic = 'косметический'
    without_repair = 'без ремонта'
    european_quality = 'евроремонт'
    fine_finish = 'чистовой'
    designer = 'дизайнерский'
    shell_and_core = 'черновой'
    missing = 'пропущено'
