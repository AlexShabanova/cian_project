import sqlite3
from typing import List

from application.db.dataaccessobjects.ad_data_dao import AdDataDao
from application.db.dataaccessobjects.links_dao import LinksDao


class DatabaseManager:
    """При создании объекта класса осуществиться подключение к бд или создастся бд,
     затем проверка или создание таблицы LINKS"""

    def __init__(self):
        self.__db = sqlite3.connect(r'application\db\cian.db')  # ссылка на файл бд
        LinksDao.init_links_table(self.__db)
        AdDataDao.init_ads_table(self.__db)

    def insert_link_into_links(self, link):
        """Сохранение ссылки в таблицу links"""
        LinksDao.insert_link(self.__db, link)

    def set_link_processed(self, link):
        """Данные по сссылке скачаны"""
        LinksDao.set_link_processed(self.__db, link)

    def get_links_from_db(self) -> List[str]:
        """Получение всех ссылок из БД"""
        return LinksDao.select_all_links(self.__db)

    def insert_ad_data(self, link, flat_type, rooms, price, price_per_meter, sale_type, mortgage, area,
                       living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller,
                       built_year_again, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                       finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                       housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply,
                       description_text):
        """Сохранение данных одного объявления"""
        AdDataDao.insert_ad_data(self.__db, link, flat_type, rooms, price, price_per_meter, sale_type, mortgage, area,
                       living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller,
                       built_year_again, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                       finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                       housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply,
                       description_text)

