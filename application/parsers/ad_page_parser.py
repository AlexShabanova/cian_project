from locale import atof, setlocale, LC_NUMERIC
from typing import List, Tuple, Any, Dict, Union

from bs4 import BeautifulSoup
from bs4 import Tag


class AdPageParser:

    def __init__(self, page_source: str):
        self.soup = BeautifulSoup(page_source, 'lxml')

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

    def get_price_per_meter(self) -> int:
        """Получение цены за квадратный метр"""
        price_per_meter = None
        try:
            price_per_meter_row = self.soup.find('span', {
                'class': 'a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_5u--cJ35s a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_14px--TCfeJ a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__nowrap--Akbtc'}).text[
                                  :-5]
            price_per_meter = int(price_per_meter_row.replace(' ', ''))
        except Exception as err:
            pass

        return price_per_meter


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
                              flat_summary_values: List[Tag]) -> List[Union[int, float]]:
        """Получение краткой информации о квартире (площаль, этажность, год постройки и пр.)"""
        setlocale(LC_NUMERIC, 'ru')
        area, living_area, kitchen_area, floor, floors, built_year = None, None, None, None, None, None
        for title_value in zip(flat_summary_names, flat_summary_values):
            if title_value[0].text == 'Общая':
                area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Жилая':
                living_area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Кухня':
                kitchen_area = atof(title_value[1].text.split('\xa0')[0])
            elif title_value[0].text == 'Этаж':
                floor, floors = int(title_value[1].text.split(' ')[0]), int(title_value[1].text.split(' ')[-1])
            elif title_value[0].text == 'Построен':
                built_year = int(title_value[1].text)
            elif title_value[0].text == 'Срок сдачи':
                built_year = int(title_value[1].text.split(' ')[-1])
        return [area, living_area, kitchen_area, floor, floors, built_year]

    def get_address_and_district(self) -> Tuple[str, Any]:
        """Район и полный адрес (для проверки одинаковых объявлений)"""
        address, district = None, None
        try:
            address_list = self.soup.find_all('a', {'data-name': 'Link',
                                                    'class': 'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})
            address = ','.join(elem.text for elem in address_list)
            district = address_list[1].text
        except Exception as err:
            pass

        return address, district


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

    def get_flat_general_info(self, names_values_dict: Dict[str, str]) -> List[Union[str, float]]:
        """Получение общей информации о квартире (Тип жилья, Планировка, Высота потолков,
         Санузел, Балкон/лоджия, Ремонт, Вид из окон, Отделка)"""
        housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition = None, None, None, None, None, None, None, None

        for name, value in names_values_dict.items():
            if name == 'Тип жилья':
                if 'Вторичка' in value:
                    housing_type = 'вторичное'
                elif 'Новостройка' in value:
                    housing_type = 'новостройка'
            elif name == 'Планировка':
                if 'Изолированная' in value:
                    planning = 'изолированная'
                elif 'Смежная' in value:
                    planning = 'смежная'
                elif 'Смежно-изолированная' in value:
                    planning = 'смежно-изолированная'
            elif name == 'Высота потолков':
                ceiling_height = atof(value.split(' ')[0])
            elif name == 'Санузел':
                bathroom = value
            elif name == 'Балкон/лоджия':
                balcony_loggia = value
            elif name == 'Ремонт':
                if 'Без ремонта' in value:
                    repair = 'без ремонта'
                elif 'Евроремонт' in value:
                    repair = 'евроремонт'
                elif 'Косметический' in value:
                    repair = 'косметический'
                elif 'Дизайнерский' in value:
                    repair = 'дизайнерский'
            elif name == 'Вид из окон':
                if 'Во двор' in value:
                    view = 'во двор'
                elif 'На улицу' in value:
                    view = 'на улицу'
                elif 'На улицу и двор' in value:
                    view = 'на улицу и двор'
            elif name == 'Отделка':
                if 'Черновая' in value:
                    view = 'черновая'
                elif 'Чистовая' in value:
                    view = 'чистовая'
                elif 'Предчистовая' in value:
                    view = 'предчистовая'
                elif 'Нет' in value:
                    view = 'нет'
        return [housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                finished_shell_condition]

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

    def get_house_info(self, names_values_dict: Dict[str, str]) -> List[Union[str, int]]:
        """Получение информации о доме"""
        built_year, house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply = \
            None, None, None, None, None, None, None, None, None, None, None, None, None
        for name, value in names_values_dict.items():
            if name == 'Год постройки':
                built_year = int(value)
            if name == 'Тип дома':
                house_type = value.lower()
            elif name == 'Класс':
                house_class = value.lower()
            elif name == 'Кол-во корпусов':
                building_number = int(value.split(' ')[0])
            elif name == 'Парковка':
                parking = value.lower()
            elif name == 'Лифты':
                elevators = value.lower()
            elif name == 'Строительная серия':
                housing_line = value.lower()
            elif name == 'Тип перекрытий':
                floor_type = value.lower()
            elif name == 'Подъезды':
                entrance_number = int(value)
            elif name == 'Отопление':
                heating = value.lower()
            elif name == 'Аварийность':
                unsafe_house = value.lower()
            elif name == 'Мусоропровод':
                garbage_disposal = value.lower()
            elif name == 'Газоснабжение':
                gas_supply = value.lower()
        return [built_year, house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number,
                heating, unsafe_house, garbage_disposal, gas_supply]

    def get_description_text(self) -> str:
        """Получение текста объявления"""
        try:
            return self.soup.find('p', {'itemprop': 'description',
                                        'class': 'a10a3f92e9--description-text--YNzWU'}).text
        except Exception as err:
            pass
