import random

from application.datamodel.data_models import DealType, OfferType, Region
from application.db.database_manager import DatabaseManager
from application.httpclient.httpclient import HttpClient
from application.parsers.ad_page_parser import AdPageParser
from application.parsers.main_page_parser import MainPageParser


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        self.database_manager = DatabaseManager()
        self.http_client = HttpClient()

    def get_links_from_page(self):
        """Получение списка ссылок на объявления с главной страницы
        Обработка ошибок: если приходит пустой лист, лист None, конец номеров страниц, ссылка есть в бд """
        page_number = 1
        last_page = False
        while last_page is False:
            print(f"Текущий номер страницы: {page_number}")
            link = f"https://www.cian.ru/cat.php?deal_type={self.deal_type.value}&engine_version=2&offer_type={self.offer_type.value}&p={page_number}&region={self.region.value}"
            print(link)
            page_source = self.http_client.get_page_source(link)

            # while 'captcha' in page_source:
            #     time.sleep(30)

            links_from_page = MainPageParser.parse_links_from_main_page(page_source)
            print(f"Ссылки со страницы: {links_from_page}")
            links_from_db = self.database_manager.get_links_from_db()
            check = all(link in links_from_db for link in links_from_page)
            if check is True:
                last_page = True
            else:
                for link in links_from_page:
                    if link not in links_from_db:
                        self.database_manager.insert_link_into_links(link)
                page_number += 1

        print('Закончили получать ссылки со страниц')

    def get_ad_data_from_all_links(self):
        """Получение данных со страницы объявления"""
        all_links = self.database_manager.get_links_from_db()
        links_len = len(all_links)
        for i, link in enumerate(all_links):
            try:
                print(f"Текущая ссылка: {link}, {i + 1} из {links_len}")
                page_source = self.http_client.get_page_source(link)
                ad_parser = AdPageParser(page_source)
                titles = ad_parser.get_titles()
                flat_type = ad_parser.get_flat_type(titles)
                rooms = ad_parser.get_number_of_rooms(titles)
                price = ad_parser.get_price()
                price_per_meter = ad_parser.get_price_per_meter()
                sale_type = ad_parser.get_sale_type()
                mortgage = ad_parser.get_mortgage()
                flat_summary_names = ad_parser.get_flat_summary_names()
                flat_summary_values = ad_parser.get_flat_summary_values()
                area, living_area, kitchen_area, floor, floors, built_year = ad_parser.get_flat_summary_info(
                    flat_summary_names, flat_summary_values)
                address, district = ad_parser.get_address_and_district()
                metro_station = ad_parser.get_metro_station()
                seller = ad_parser.get_seller()
                flat_general_info_names_values = ad_parser.get_flat_general_info_names_values()
                slovar = ad_parser.get_flat_general_info(flat_general_info_names_values)
                housing_type = slovar['']
                housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition = ad_parser.get_flat_general_info(
                    flat_general_info_names_values)
                house_info_names_values = ad_parser.get_house_info_names_values()
                built_year_again, house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply = ad_parser.get_house_info(
                    house_info_names_values)
                description_text = ad_parser.get_description_text()
                self.database_manager.insert_ad_data(link, flat_type, rooms, price, price_per_meter, sale_type,
                                                     mortgage,
                                                     area, living_area, kitchen_area, floor, floors, built_year,
                                                     address,
                                                     district, metro_station, seller, housing_type,
                                                     planning,
                                                     ceiling_height, bathroom, balcony_loggia,
                                                     repair, view, finished_shell_condition, built_year_again,
                                                     house_type, house_class,
                                                     building_number,
                                                     parking, elevators, housing_line, floor_type, entrance_number,
                                                     heating,
                                                     unsafe_house,
                                                     garbage_disposal, gas_supply, description_text)
                self.database_manager.set_link_processed(link)
            except Exception as err:
                print(err)
        print("Все ссылки обработаны")

    def generate_fake_ad_data(self, n):
        for i in range(n):
            link = f"fake link '{i}'"

            flat_type = random.choice(['апартаменты', 'квартира'])

            rooms = random.choice([-1, 0, 1, 2, 3, 4, 5, 6])

            price = random.randint(1_000_000, 100_000_000)

            # price_per_meter = ad_parser.get_price_per_meter() после living_area?
            # r2 = random.randint(0, 100_000_000)
            # price = None
            # if r2 >= 1_000_000:
            #     price = r2

            sale_type = random.choice(['долевое участие (214-фз)', 'альтернатива', 'свободная продажа'])

            mortgage = random.choice([True, False])

            area = round(random.uniform(10, 100), 2)
            living_area = round(random.uniform(5, area), 2)
            kitchen_area = round(random.uniform(1, area), 2)
            floors = random.randint(2, 50)
            floor = random.randint(1, floors)
            built_year = random.randint(1800, 2022)
            price_per_meter = round(price / area)

            address = f"fake address '{i}'"
            district = random.choice(['ЦАО', 'ВАО', 'СВАО', 'САО', 'СЗАО', 'ЗАО', 'ЮЗАО', 'ЮАО', 'ЮВАО'])

            metro_station = random.choice(['Международная',
                                           'Студенческая',
                                           'Кутузовская',
                                           'Фили',
                                           'Багратионовская',
                                           'Филевский парк',
                                           'Пионерская',
                                           'Кунцевская',
                                           'Алтуфьево',
                                           'Бибирево',
                                           'Отрадное',
                                           'Владыкино',
                                           'Петровско - Разумовская',
                                           'Тимирязевская',
                                           'Дмитровская',
                                           'Савеловская',
                                           'Менделеевская',
                                           'Цветной бульвар',
                                           'Чеховская',
                                           'Боровицкая',
                                           'Полянка',
                                           'Серпуховская',
                                           'Тульская',
                                           'Нагатинская',
                                           'Нагорная',
                                           'Нахимовский проспект',
                                           'Севастопольская',
                                           'Чертановская',
                                           'Южная',
                                           'Пражская',
                                           'Улица Академика Янгеля',
                                           'Аннино',
                                           'Бульвар Дмитрия Донского'
                                           ])

            seller = random.choice(['не указано', 'застройщик', f"random seller '{i}'"])

            housing_type = random.choice(['вторичное', 'новостройка', None])
            planning = random.choice(['изолированная', 'смежная', 'смежно-изолированная', None])
            ceiling_height = round(random.uniform(2, 4), 2)
            bathroom = f"bathroom '{i}'"
            balcony_loggia = f"balcony_loggia '{i}'"
            repair = random.choice(['без ремонта', 'евроремонт', 'косметический', 'дизайнерский', None])
            view = random.choice(['во двор', 'на улицу', 'на улицу и двор', None])
            finished_shell_condition = random.choice(['черновая', 'чистовая', 'предчистовая', 'нет', None])


            house_type = random.choice(['монолитный', 'панельный', None])
            house_class = random.choice(['премиум', 'бизнес', None])
            building_number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None])
            parking = random.choice(['подземная', 'наземная', 'стихийная', None])
            elevators = f"elevators '{i}'"
            housing_line = f"housing_line '{i}'"
            floor_type = random.choice(['деревянные', 'железобетонные', None])
            entrance_number = random.randint(1, 15)
            heating = f"heating '{i}'"
            unsafe_house = random.choice(['да', 'нет', None])
            garbage_disposal = random.choice(['да', 'нет', None])
            gas_supply = random.choice(['да', 'нет', None])

            description_text = f"description text '{i}'"

            self.database_manager.insert_ad_data(link, flat_type, rooms, price, price_per_meter, sale_type, mortgage, area,
                       living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller,
                       housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                       finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                       housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply,
                       description_text)

            print(f"Сгенерированно '{i + 1}'/'{n}'")

    def update_incorrect_values(self):
        self.database_manager.update_incorrect_columns()
