import sqlite3
from typing import List

from application.db.dataaccessobjects.ad_data_dao import AdDataDao
from application.db.dataaccessobjects.filters_dao import FiltersDao
from application.db.dataaccessobjects.links_dao import LinksDao


class DatabaseManager:
    """При создании объекта класса осуществиться подключение к бд или создастся бд,
     затем проверка или создание таблицы LINKS"""

    def __init__(self):
        self.__db = sqlite3.connect(r'application\db\cian.db')  # ссылка на файл бд
        LinksDao.init_links_table(self.__db)
        AdDataDao.init_ads_table(self.__db)
        FiltersDao.init_filters_table(self.__db)

    def insert_link_into_links(self, link):
        """Сохранение ссылки в таблицу links"""
        LinksDao.insert_link(self.__db, link)

    def set_link_processed(self, link):
        """Данные по сссылке скачаны"""
        LinksDao.set_link_processed(self.__db, link)

    def get_unprocessed_links_from_db(self) -> List[str]:
        """Получение всех необработанных ссылок из БД"""
        return LinksDao.select_all_unprocessed_links(self.__db)

    def insert_ad_data(self, link, flat_type, rooms, price, sale_type, mortgage, area,
                       living_area, kitchen_area, floor, floors, build_year, address, district, metro_station, seller,
                       housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                       finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                       housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply,
                       description_text, is_suspicious):
        """Сохранение данных одного объявления"""
        AdDataDao.insert_ad_data(self.__db, link, flat_type, rooms, price, sale_type, mortgage, area,
                                 living_area, kitchen_area, floor, floors, build_year, address, district, metro_station,
                                 seller,
                                 housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                                 finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                                 housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal,
                                 gas_supply,
                                 description_text, is_suspicious)

    def update_incorrect_columns(self):
        AdDataDao.change_column_values(self.__db)

    def get_all_processed_filters(self) -> List[int]:
        return FiltersDao.get_all_processed_filters(self.__db)

    def insert_processed_filter(self, processed_filter):
        FiltersDao.insert_processed_filter(self.__db, processed_filter)
