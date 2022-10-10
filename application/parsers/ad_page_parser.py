from locale import atof, setlocale, LC_NUMERIC
from typing import List, Tuple, Any, Dict

from bs4 import BeautifulSoup
from bs4 import Tag

from application.parsers.models.AddressAndDistrict import AddressAndDistrict
from application.parsers.models.FlatGeneralInfo import FlatGeneralInfo
from application.parsers.models.FlatSummaryInfo import FlatSummaryInfo
from application.parsers.models.HouseInfo import HouseInfo


class AdPageParser:

    def __init__(self, page_source: str):
        self.soup = BeautifulSoup(page_source, 'lxml')
        self.page_source = page_source

    def get_titles(self) -> Tuple[str, Any]:
        title_row = self.soup.find('meta', {'property': 'og:title'}).get('content')
        title = title_row.lower().split('за')[0]
        ad_title = self.soup.find('h1', {'class': 'a10a3f92e9--title--UEAG3'}).text
        return title, ad_title

    def get_flat_type(self, titles: Tuple[str, Any]) -> str:
        """Получение типа: квартира или апартаменты"""
        flat_type = None
        try:
            if 'апартаменты' in titles[0]:
                flat_type = 'апартаменты'
            else:  # если квартира или (квартира-)студия
                flat_type = 'квартира'
        except Exception as err:
            pass

        return flat_type

    def get_number_of_rooms(self, titles: Tuple[str, Any]) -> int:
        """Получение количества комнат: 1-6-комнатные,свободная планировка (-1) или студия (0)"""
        number_of_rooms = None
        try:
            if 'студия' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 0
            elif '1' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 1
            elif '2' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 2
            elif '3' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 3
            elif '4' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 4
            elif '5' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 5
            elif '6' in titles[0] or 'студия' in titles[1]:
                number_of_rooms = 6
            else:
                number_of_rooms = -1
        except Exception as err:
            pass

        return number_of_rooms

    def get_price(self) -> int:
        """Получение цены за квартиру"""
        price = None
        try:
            price_row = self.soup.find('span', {'itemprop': 'price'}).get('content')[:-2]
            price = int(price_row.replace(' ', ''))
        except Exception as err:
            pass

        return price


    def get_sale_type(self) -> str:
        """Получение типа продажи: свободная, альтернатива, долевое участие"""
        sale_type = None
        try:
            sale_type_row = self.soup.find('p', {'class': 'a10a3f92e9--description--CPyUa'}).getText().lower().replace(
                '\xa0',
                ' ')
            try:
                if 'свободная продажа' in sale_type_row:
                    sale_type = 'свободная продажа'
                elif 'альтернатива' in sale_type_row:
                    sale_type = 'альтернатива'
                elif 'долевое участие (214-фз)' in sale_type_row:
                    sale_type = 'долевое участие (214-фз)'
            except Exception as err:
                pass
        except Exception as err:
            pass

        return sale_type

    def get_mortgage(self) -> bool:
        """Возможность ипотеки/рассрочки"""
        mortgage = False
        try:
            sale_type_row = self.soup.find('p', {'class': 'a10a3f92e9--description--CPyUa'}).getText().lower().replace(
                '\xa0',
                ' ')
            if 'ипотек' in sale_type_row:
                mortgage = True
        except Exception as err:
            pass

        try:
            promo_label_row = self.soup.find('span', {
                'class': 'a10a3f92e9--label--fCs_v a10a3f92e9--color_white_100--YUO3d a10a3f92e9--background_error_100--ws65v'}).find(
                'span').text.lower()
            if 'ипотек' in promo_label_row:
                mortgage = True
            elif 'рассрочк' in promo_label_row:
                mortgage = True
        except Exception as err:
            pass

        return mortgage

    def get_flat_summary_names(self) -> List[Tag]:
        """Получение заголовков в блоке краткого описания (площаль, этажность, год постройки и пр.)"""
        try:
            return self.soup.find_all('div', {'data-testid': 'object-summary-description-title',
                                              'class': 'a10a3f92e9--info-title--JWtIm'})
        except Exception as err:
            return []

    def get_flat_summary_values(self) -> List[Tag]:
        """Получение значений для заголовков в блоке краткого описания (площаль, этажность, год постройки и пр.)"""
        try:
            return self.soup.find_all('div', {'data-testid': 'object-summary-description-value',
                                              'class': 'a10a3f92e9--info-value--bm3DC'})
        except Exception as err:
            return []

    def get_flat_summary_info(self, flat_summary_names: List[Tag],
                              flat_summary_values: List[Tag]) -> FlatSummaryInfo:
        """Получение краткой информации о квартире (площаль, этажность, год постройки и пр.)"""
        setlocale(LC_NUMERIC, 'ru')
        result = FlatSummaryInfo()
        for title_value in zip(flat_summary_names, flat_summary_values):
            if title_value[0].text == 'Общая':
                result.area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Жилая':
                result.living_area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Кухня':
                result.kitchen_area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Этаж':
                result.floor = int(title_value[1].text.split(' ')[0])
                result.floors = int(title_value[1].text.split(' ')[-1])
            elif title_value[0].text == 'Построен':
                result.built_year = int(title_value[1].text)
            elif title_value[0].text == 'Срок сдачи':
                result.built_year = int(title_value[1].text.split(' ')[-1])
            elif title_value[0].text == 'Сдан':
                result.built_year = int(title_value[1].text.split(' ')[-1])
        return result

    def get_address_and_district(self) -> AddressAndDistrict:
        """Район и полный адрес (для проверки одинаковых объявлений)"""
        result = AddressAndDistrict()
        try:
            address_list = self.soup.find_all('a', {'data-name': 'Link',
                                                    'class': 'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})
            result.address = ','.join(elem.text for elem in address_list)
            result.district = address_list[1].text
        except Exception as err:
            pass

        return result


    def get_metro_station(self) -> str:
        """Ближайшая станция метро"""
        metro_station = None
        try:
            metro_station = self.soup.find('a', {'class': 'a10a3f92e9--underground_link--Sxo7K'}).text
        except Exception as err:
            pass
        return metro_station

    def get_seller(self) -> str:
        seller = 'не указано'
        try:
            seller_check = self.soup.find('span', {'data-name': 'Tag',
                                                   'class': 'a10a3f92e9--tag--X46ci a10a3f92e9--tag--dqqQK'}).text.lower()
            if seller_check == 'застройщик':
                seller = 'застройщик'
        except Exception as err:
            pass

        try:
            seller_check = self.soup.find('div', {'class': 'a10a3f92e9--title--YaRYv'}).text.lower()
            if seller_check == 'собственник':
                seller = 'собственник'
        except Exception as err:
            pass

        try:
            seller_check = self.soup.find('span', {
                'class': 'a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_4u--fix4Q a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_10px--Ccu1C a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_textTransform__uppercase--sMMpu'}).text.lower()
            if seller_check == 'агентство недвижимости':
                seller = 'агентство'
        except Exception as err:
            pass

        try:
            seller_check = self.soup.find('h4', {'class': 'a10a3f92e9--title--JhS0L'}).text
            if seller_check:
                seller = 'частный риелтор'
        except Exception as err:
            pass

        try:
            seller_check = self.soup.find('span', {'data-name': 'Tag',
                                                   'class': 'a10a3f92e9--tag--X46ci a10a3f92e9--tag--dqqQK'}).text.lower()
            if seller_check == 'консультант':
                seller = 'консультант'
        except Exception as err:
            pass

        return seller

    def get_flat_general_info_names_values(self) -> Dict[str, str]:
        """Получение заголовков и значений блока информации о квартире"""
        names_values_dict = dict()
        try:
            flat_information = self.soup.find_all('li', class_='a10a3f92e9--item--d9uzC')
            for el in flat_information:
                try:
                    name = el.find('span',
                                   class_='a10a3f92e9--name--x7_lt').text
                    value = el.find('span',
                                    class_='a10a3f92e9--value--Y34zN').text
                    names_values_dict[name] = value
                except Exception as err:
                    pass
        except Exception as err:
            pass
        return names_values_dict

    def get_flat_general_info(self, names_values_dict: Dict[str, str]) -> FlatGeneralInfo:
        """Получение общей информации о квартире (Тип жилья, Планировка, Высота потолков,
         Санузел, Балкон/лоджия, Ремонт, Вид из окон, Отделка)"""
        result = FlatGeneralInfo()

        for name, value in names_values_dict.items():
            if name == 'Тип жилья':
                if 'Вторичка' in value:
                    result.housing_type = 'вторичное'
                elif 'Новостройка' in value:
                    result.housing_type = 'новостройка'
            elif name == 'Планировка':
                if 'Изолированная' in value:
                    result.planning = 'изолированная'
                elif 'Смежная' in value:
                    result.planning = 'смежная'
                elif 'Смежно-изолированная' in value:
                    result.planning = 'смежно-изолированная'
            elif name == 'Высота потолков':
                result.ceiling_height = atof(value.split(' ')[0])
            elif name == 'Санузел':
                result.bathroom = value
            elif name == 'Балкон/лоджия':
                result.balcony_loggia = value
            elif name == 'Ремонт':
                if 'Без ремонта' in value:
                    result.repair = 'без ремонта'
                elif 'Евроремонт' in value:
                    result.repair = 'евроремонт'
                elif 'Косметический' in value:
                    result.repair = 'косметический'
                elif 'Дизайнерский' in value:
                    result.repair = 'дизайнерский'
            elif name == 'Вид из окон':
                if 'Во двор' in value:
                    result.view = 'во двор'
                elif 'На улицу' in value:
                    result.view = 'на улицу'
                elif 'На улицу и двор' in value:
                    result.view = 'на улицу и двор'
            elif name == 'Отделка':
                if 'Черновая' in value:
                    result.finished_shell_condition = 'черновая'
                elif 'Чистовая' in value:
                    result.finished_shell_condition = 'чистовая'
                elif 'Предчистовая' in value:
                    result.finished_shell_condition = 'предчистовая'
                elif 'Нет' in value:
                    result.finished_shell_condition = 'нет'
        return result

    def get_house_info_names_values(self) -> Dict[str, str]:
        """Получение заголовков и значений блока информации о доме"""
        names_values_dict = dict()
        #  для новостроек
        try:
            house_information_new_build = self.soup.find_all('li', class_='a10a3f92e9--item--E1gcC')
            for el in house_information_new_build:
                try:
                    name = el.find('span',
                                   class_='a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_22px--bnKK9 a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_inline--bMJq9 a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__normal--xbqP6').text
                    value = el.find('span',
                                    class_='a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_inline--bMJq9 a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__normal--xbqP6').text
                    names_values_dict[name] = value
                except Exception as err:
                    pass
        except Exception as err:
            pass

        #  для вторичного жилья
        try:
            house_information_secondary_housing = self.soup.find_all('div', {'data-name': 'Item',
                                                                             'class': 'a10a3f92e9--item--M4jGb'})
            for el in house_information_secondary_housing:
                try:
                    name = el.find('div', class_='a10a3f92e9--name--pLPu9').text
                    value = el.find('div', class_='a10a3f92e9--value--G2JlN').text
                    names_values_dict[name] = value
                except Exception as err:
                    pass
        except Exception as err:
            pass

        return names_values_dict

    def get_house_info(self, names_values_dict: Dict[str, str]) -> HouseInfo:
        """Получение информации о доме"""
        result = HouseInfo()
        for name, value in names_values_dict.items():
            if name == 'Год постройки':
                result.built_year = int(value)
            if name == 'Тип дома':
                result.house_type = value.lower()
            elif name == 'Класс':
                result.house_class = value.lower()
            elif name == 'Кол-во корпусов':
                result.building_number = int(value.split(' ')[0])
            elif name == 'Парковка':
                result.parking = value.lower()
            elif name == 'Лифты':
                result.elevators = value.lower()
            elif name == 'Строительная серия':
                result.housing_line = value.lower()
            elif name == 'Тип перекрытий':
                result.floor_type = value.lower()
            elif name == 'Подъезды':
                result.entrance_number = int(value)
            elif name == 'Отопление':
                result.heating = value.lower()
            elif name == 'Аварийность':
                result.unsafe_house = value.lower()
            elif name == 'Мусоропровод':
                result.garbage_disposal = value.lower()
            elif name == 'Газоснабжение':
                result.gas_supply = value.lower()
        return result

    def get_description_text(self) -> str:
        """Получение текста объявления"""
        try:
            return self.soup.find('p', {'itemprop': 'description',
                                        'class': 'a10a3f92e9--description-text--YNzWU'}).text
        except Exception as err:
            pass

    def is_ad_suspicious(self) -> int:
        """Проверка, содержит ли объявление маркировку об ошибках (подозрительное объявление)"""
        if 'В объявлениях этого агента встречаются ошибки' in self.page_source:
            return 1
        else:
            return 0