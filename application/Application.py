import threading
import time
from collections import defaultdict
from multiprocessing.dummy import Pool

from application.datamodel.data_models import DealType, OfferType, Region, ObjectType, RoomType
from application.db.database_manager import DatabaseManager
from application.httpclient.httpclient import HttpClient
from application.parsers.ad_page_parser import AdPageParser
from application.parsers.main_page_parser import MainPageParser


class Application:

    def __init__(
            self,
            db_manager: DatabaseManager,
            deal_type: DealType,
            offer_type: OfferType,
            region: Region,
            object_type: ObjectType,
            room: RoomType,
            minprice: int,
            maxprice: int,
    ):
        # Parameters for main page link generation
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        self.room = room
        self.minprice = minprice
        self.maxprice = maxprice
        self.object_type = object_type

        # Instances for db and network interaction
        self.database_manager = db_manager
        self.http_client = HttpClient()

        self.db_manager_for_thread = defaultdict(DatabaseManager)
        self.http_client_for_thread = defaultdict(HttpClient)

    def get_links_from_page(self):
        """Получение списка ссылок на объявления с главной страницы
        Обработка ошибок: если приходит пустой лист, лист None, конец номеров страниц, ссылка есть в бд """
        page_number = 1
        last_page = False
        while last_page is False:
            link = f"https://www.cian.ru/cat.php?deal_type={self.deal_type.value}" \
                   f"&engine_version=2&offer_type={self.offer_type.value}" \
                   f"&p={page_number}" \
                   f"&region={self.region.value}" \
                   f"&room{self.room.value}=1" \
                   f"&object_type%5B0%5D={self.object_type.value}" \
                   f"&minprice={self.minprice}" \
                   f"&maxprice={self.maxprice}" \
                   # f"&sort=creation_date_desc"  # сортировка объявлений "сначала новые"
            page_source = self.http_client.get_page_source(link)

            if 'По такому запросу объявления еще не разместили' in page_source:
                print("С такими параметрами ничего не нашлось")
                break

            while 'captcha' in page_source:
                print("captcha")
                # os.system("shutdown /s /t 0")
                time.sleep(30)
                page_source = self.http_client.get_page_source(link)

            links_from_page = MainPageParser.parse_links_from_main_page(page_source)
            links_from_db = self.database_manager.get_unprocessed_links_from_db()
            print(f"страница = {page_number}, количество ссылок на странице = {len(links_from_page)}, в БД = {len(links_from_db)}")

            check = all(link in links_from_db for link in links_from_page)
            if check is True:
                last_page = True
            else:
                for link in links_from_page:
                    if link not in links_from_db:
                        self.database_manager.insert_link_into_links(link)
                page_number += 1

    def get_ad_data_from_all_links(self):
        """Получение данных со страницы объявления"""
        all_links = self.database_manager.get_unprocessed_links_from_db()
        links_len = len(all_links)
        for i, link in enumerate(all_links):
            try:
                print(f"Текущая ссылка: {link}, {i + 1} из {links_len}")
                page_source = self.http_client.get_page_source(link)
                while 'captcha' in page_source and '/recaptcha' not in page_source:
                    print("captcha")
                    # os.system("shutdown /s /t 0")
                    time.sleep(30)
                    page_source = self.http_client.get_page_source(link)
                ad_parser = AdPageParser(page_source)
                titles = ad_parser.get_titles()
                flat_type = ad_parser.get_flat_type(titles)
                rooms = ad_parser.get_number_of_rooms(titles)
                price = ad_parser.get_price()
                sale_type = ad_parser.get_sale_type()
                mortgage = ad_parser.get_mortgage()
                flat_summary_names = ad_parser.get_flat_summary_names()
                flat_summary_values = ad_parser.get_flat_summary_values()
                flat_summary_info = ad_parser.get_flat_summary_info(
                    flat_summary_names, flat_summary_values)
                address_and_district = ad_parser.get_address_and_district()
                metro_station = ad_parser.get_metro_station()
                seller = ad_parser.get_seller()
                flat_general_info_names_values = ad_parser.get_flat_general_info_names_values()
                flat_general_info = ad_parser.get_flat_general_info(
                    flat_general_info_names_values)
                house_info_names_values = ad_parser.get_house_info_names_values()
                house_info = ad_parser.get_house_info(house_info_names_values)

                description_text = ad_parser.get_description_text()

                is_suspicious = ad_parser.is_ad_suspicious()

                build_year_resolved = None
                if flat_summary_info.built_year is not None:
                    build_year_resolved = flat_summary_info.built_year
                else:
                    build_year_resolved = house_info.built_year

                self.database_manager.insert_ad_data(link=link, flat_type=flat_type, rooms=rooms, price=price,
                                                     sale_type=sale_type,
                                                     mortgage=mortgage,
                                                     area=flat_summary_info.area,
                                                     living_area=flat_summary_info.living_area,
                                                     kitchen_area=flat_summary_info.kitchen_area,
                                                     floor=flat_summary_info.floor,
                                                     floors=flat_summary_info.floors, build_year=build_year_resolved,
                                                     address=address_and_district.address,
                                                     district=address_and_district.district,
                                                     metro_station=metro_station, seller=seller,
                                                     housing_type=flat_general_info.housing_type,
                                                     planning=flat_general_info.planning,
                                                     ceiling_height=flat_general_info.ceiling_height,
                                                     bathroom=flat_general_info.bathroom,
                                                     balcony_loggia=flat_general_info.balcony_loggia,
                                                     repair=flat_general_info.repair, view=flat_general_info.view,
                                                     finished_shell_condition=flat_general_info.finished_shell_condition,
                                                     house_type=house_info.house_type,
                                                     house_class=house_info.house_class,
                                                     building_number=house_info.building_number,
                                                     parking=house_info.parking, elevators=house_info.elevators,
                                                     housing_line=house_info.housing_line,
                                                     floor_type=house_info.floor_type,
                                                     entrance_number=house_info.entrance_number,
                                                     heating=house_info.heating,
                                                     unsafe_house=house_info.unsafe_house,
                                                     garbage_disposal=house_info.garbage_disposal,
                                                     gas_supply=house_info.gas_supply,
                                                     description_text=description_text,
                                                     is_suspicious=is_suspicious)
                self.database_manager.set_link_processed(link)
            except Exception as err:
                print(f"Ошибка в get_ad_data_from_all_links(), {err}")
        print("Все ссылки обработаны")


    def get_info_from_one_link(self, link):
        try:
            thread_id = str(threading.get_ident())
            print(f"Обрабатывается ссылка {link} в потоке {thread_id}")
            page_source = self.http_client_for_thread[thread_id].get_page_source(link)
            while 'captcha' in page_source and '/recaptcha' not in page_source:
                print("captcha")
                # os.system("shutdown /s /t 0")
                time.sleep(30)
                page_source = self.http_client_for_thread[thread_id].get_page_source(link)
            ad_parser = AdPageParser(page_source)
            titles = ad_parser.get_titles()
            flat_type = ad_parser.get_flat_type(titles)
            rooms = ad_parser.get_number_of_rooms(titles)
            price = ad_parser.get_price()
            sale_type = ad_parser.get_sale_type()
            mortgage = ad_parser.get_mortgage()
            flat_summary_names = ad_parser.get_flat_summary_names()
            flat_summary_values = ad_parser.get_flat_summary_values()
            flat_summary_info = ad_parser.get_flat_summary_info(
                flat_summary_names, flat_summary_values)
            address_and_district = ad_parser.get_address_and_district()
            metro_station = ad_parser.get_metro_station()
            seller = ad_parser.get_seller()
            flat_general_info_names_values = ad_parser.get_flat_general_info_names_values()
            flat_general_info = ad_parser.get_flat_general_info(
                flat_general_info_names_values)
            house_info_names_values = ad_parser.get_house_info_names_values()
            house_info = ad_parser.get_house_info(house_info_names_values)

            description_text = ad_parser.get_description_text()

            is_suspicious = ad_parser.is_ad_suspicious()

            build_year_resolved = None
            if flat_summary_info.built_year is not None:
                build_year_resolved = flat_summary_info.built_year
            else:
                build_year_resolved = house_info.built_year

            self.db_manager_for_thread[thread_id].insert_ad_data(link=link, flat_type=flat_type, rooms=rooms, price=price,
                                                 sale_type=sale_type,
                                                 mortgage=mortgage,
                                                 area=flat_summary_info.area,
                                                 living_area=flat_summary_info.living_area,
                                                 kitchen_area=flat_summary_info.kitchen_area,
                                                 floor=flat_summary_info.floor,
                                                 floors=flat_summary_info.floors, build_year=build_year_resolved,
                                                 address=address_and_district.address,
                                                 district=address_and_district.district,
                                                 metro_station=metro_station, seller=seller,
                                                 housing_type=flat_general_info.housing_type,
                                                 planning=flat_general_info.planning,
                                                 ceiling_height=flat_general_info.ceiling_height,
                                                 bathroom=flat_general_info.bathroom,
                                                 balcony_loggia=flat_general_info.balcony_loggia,
                                                 repair=flat_general_info.repair, view=flat_general_info.view,
                                                 finished_shell_condition=flat_general_info.finished_shell_condition,
                                                 house_type=house_info.house_type,
                                                 house_class=house_info.house_class,
                                                 building_number=house_info.building_number,
                                                 parking=house_info.parking, elevators=house_info.elevators,
                                                 housing_line=house_info.housing_line,
                                                 floor_type=house_info.floor_type,
                                                 entrance_number=house_info.entrance_number,
                                                 heating=house_info.heating,
                                                 unsafe_house=house_info.unsafe_house,
                                                 garbage_disposal=house_info.garbage_disposal,
                                                 gas_supply=house_info.gas_supply,
                                                 description_text=description_text,
                                                 is_suspicious=is_suspicious)
            self.db_manager_for_thread[thread_id].set_link_processed(link)
        except Exception as err:
            print(f"Ошибка в get_ad_data_from_all_links(), {err}")

    def parsing_ad_multiprocessing(self):
        links = self.database_manager.get_unprocessed_links_from_db()
        with Pool(2) as pars:
            pars.map(self.get_info_from_one_link, links)


