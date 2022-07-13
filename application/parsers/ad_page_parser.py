from locale import atof, setlocale, LC_NUMERIC
from typing import List, Tuple, Any, Dict

from bs4 import BeautifulSoup


class AdPageParser:

    def __init__(self, page_source: str):
        self.soup = BeautifulSoup(page_source, 'lxml')

    def get_title(self):
        title_row = self.soup.find('meta', {'property': 'og:title'}).get('content')
        title = title_row.lower().split('за')[0]
        return title

    def get_flat_type(self, title: str) -> str:
        """Получение типа: квартира или апартаменты"""
        flat_type = None
        try:
            if 'апартаменты' in title:
                flat_type = 'апартаменты'
            else:  # если квартира или (квартира-)студия
                flat_type = 'квартира'
        except Exception as err:
            pass

        return flat_type

    def get_number_of_rooms(self, title: str) -> int:
        """Получение количества комнат: 1-6-комнатные,свободная планировка (-1) или студия (0)"""
        number_of_rooms = None
        try:
            if 'студия' in title:
                number_of_rooms = 0
            elif '1' in title:
                number_of_rooms = 1
            elif '2' in title:
                number_of_rooms = 2
            elif '3' in title:
                number_of_rooms = 3
            elif '4' in title:
                number_of_rooms = 4
            elif '5' in title:
                number_of_rooms = 5
            elif '6' in title:
                number_of_rooms = 6
            else:
                number_of_rooms = -1
        except Exception as err:
            pass

        return number_of_rooms

    def get_price(self) -> int:
        """Получение цены за квартиру"""
        try:
            price_row = self.soup.find('span', {'itemprop': 'price'}).get('content')[:-2]
            price = int(price_row.replace(' ', ''))
            return price
        except Exception as err:
            pass

    def get_price_per_meter(self) -> int:
        """Получение цены за квадратный метр"""
        try:
            price_per_meter_row = self.soup.find('span', {
                'class': 'a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_5u--cJ35s a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_14px--TCfeJ a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__nowrap--Akbtc'}).text[
                                  :-5]
            price_per_meter = int(price_per_meter_row.replace(' ', ''))
            return price_per_meter
        except Exception as err:
            pass

    def get_sale_type(self) -> str:
        """Получение типа продажи: свободная, альтернатива, долевое участие"""
        sale_type = None
        try:
            sale_type_row = self.soup.find('p', {'class': 'a10a3f92e9--description--CPyUa'}).getText().lower().replace(
                '\xa0',
                ' ')
            try:
                if sale_type_row == 'свободная продажа':
                    sale_type = 'свободная продажа'
                elif sale_type_row == 'альтернатива':
                    sale_type = 'альтернатива'
                elif sale_type_row == 'долевое участие (214-фз)':
                    sale_type = 'долевое участие (214-фз)'
                elif sale_type_row == 'свободная продажа, возможна ипотека':
                    sale_type = 'свободная продажа, возможна ипотека'
            except Exception as err:
                pass
        except Exception as err:
            pass

        return sale_type

    def get_mortgage(self, sale_type_row: str) -> bool:
        """Возможность ипотеки/рассрочки"""
        mortgage = False
        try:
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

    def get_flat_summary_names(self) -> List[BeautifulSoup.element.Tag]:
        """Получение заголовков в блоке краткого описания (площаль, этажность, год постройки и пр.)"""
        try:
            return self.soup.find_all('div', {'data-testid': 'object-summary-description-title',
                                              'class': 'a10a3f92e9--info-title--JWtIm'})
        except Exception as err:
            return []

    def get_flat_summary_values(self) -> List[BeautifulSoup.element.Tag]:
        """Получение значений для заголовков в блоке краткого описания (площаль, этажность, год постройки и пр.)"""
        try:
            return self.soup.find_all('div', {'data-testid': 'object-summary-description-value',
                                              'class': 'a10a3f92e9--info-value--bm3DC'})
        except Exception as err:
            return []

    def get_flat_summary_info(self, flat_summary_names: List[BeautifulSoup.element.Tag],
                              flat_summary_values: List[BeautifulSoup.element.Tag]) -> List[int, float]:
        """Получение краткой информации о квартире (площаль, этажность, год постройки и пр.)"""
        setlocale(LC_NUMERIC, 'ru')
        area, living_area, kitchen_area, floor, floors, built_date = None, None, None, None, None, None
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
                built_date = int(title_value[1].text)
            elif title_value[0].text == 'Срок сдачи':
                built_date = int(title_value[1].text.split(' ')[-1])
        return [area, living_area, kitchen_area, floor, floors, built_date]

    def get_district_and_address(self) -> Tuple[str, Any]:
        """Район и полный адрес (для проверки одинаковых объявлений)"""
        try:
            address_list = self.soup.find_all('a', {'data-name': 'Link',
                                                    'class': 'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})
            address = ','.join(elem.text for elem in address_list)
            district = address_list[1].text
            return address, district
        except Exception as err:
            pass

    def get_metro_station(self) -> str:
        """Ближайшая станция метро"""
        try:
            return self.soup.find('a', {'class': 'a10a3f92e9--underground_link--Sxo7K'}).text
        except Exception as err:
            pass

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

    def get_flat_general_info_names(self) -> List[BeautifulSoup.element.Tag]:
        """Получение заголовков блока общей информации о квартире (тип жилья, высота потолков, санузел и пр.)"""
        try:
            return self.soup.find('ul', {'class': 'a10a3f92e9--list--jHl8z'}).find_all('span', {
                'class': 'a10a3f92e9--name--x7_lt'})
        except Exception as err:
            return []

    def get_flat_general_info_values(self) -> List[BeautifulSoup.element.Tag]:
        """Получение значений для заголовков блока общей информации о квартире (тип жилья, высота потолков, санузел и пр.)"""
        try:
            return self.soup.find('ul', {'class': 'a10a3f92e9--list--jHl8z'}).find_all('span', {
                'class': 'a10a3f92e9--value--Y34zN'})
        except Exception as err:
            return []

    def get_flat_general_info(self, flat_general_info_names: List[BeautifulSoup.element.Tag],
                              flat_general_info_values: List[BeautifulSoup.element.Tag]) -> List[str, float]:
        """Получение общей информации о квартире (Тип жилья, Планировка, Высота потолков,
         Санузел, Балкон/лоджия, Ремонт, Вид из окон, Отделка)"""
        housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition = None, None, None, None, None, None, None, None

        for name_value in zip(flat_general_info_names, flat_general_info_values):
            if name_value[0].text == 'Тип жилья':
                if 'Вторичка' in name_value[1].text:
                    housing_type = 'вторичное'
                elif 'Новостройка' in name_value[1].text:
                    housing_type = 'новостройка'
            elif name_value[0].text == 'Планировка':
                if 'Изолированная' in name_value[1].text:
                    planning = 'изолированная'
                elif 'Смежная' in name_value[1].text:
                    planning = 'смежная'
                elif 'Смежно-изолированная' in name_value[1].text:
                    planning = 'смежно-изолированная'
            elif name_value[0].text == 'Высота потолков':
                ceiling_height = atof(name_value[1].text.split(' ')[0])
            elif name_value[0].text == 'Санузел':
                bathroom = name_value[1].text
            elif name_value[0].text == 'Балкон/лоджия':
                balcony_loggia = name_value[1].text
            elif name_value[0].text == 'Ремонт':
                if 'Без ремонта' in name_value[1].text:
                    repair = 'без ремонта'
                elif 'Евроремонт' in name_value[1].text:
                    repair = 'евроремонт'
                elif 'Косметический' in name_value[1].text:
                    repair = 'косметический'
                elif 'Дизайнерский' in name_value[1].text:
                    repair = 'дизайнерский'
            elif name_value[0].text == 'Вид из окон':
                if 'Во двор' in name_value[1].text:
                    view = 'во двор'
                elif 'На улицу' in name_value[1].text:
                    view = 'на улицу'
                elif 'На улицу и двор' in name_value[1].text:
                    view = 'на улицу и двор'
            elif name_value[0].text == 'Отделка':
                if 'Черновая' in name_value[1].text:
                    view = 'черновая'
                elif 'Чистовая' in name_value[1].text:
                    view = 'чистовая'
                elif 'Предчистовая' in name_value[1].text:
                    view = 'предчистовая'
                elif 'Нет' in name_value[1].text:
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

    def get_house_info(self, names_values_dict: Dict[str, str]) -> List[str, int]:
        """Получение информации о доме"""
        house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply = \
            None, None, None, None, None, None, None, None, None, None, None, None
        for name, value in names_values_dict.items():
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
        return [house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number,
                heating, unsafe_house, garbage_disposal, gas_supply]

    def get_description_text(self) -> str:
        """Получение текста объявления"""
        try:
            return self.soup.find('p', {'itemprop': 'description',
                                        'class': 'a10a3f92e9--description-text--YNzWU'}).text
        except Exception as err:
            pass
