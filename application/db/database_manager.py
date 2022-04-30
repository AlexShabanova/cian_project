import sqlite3
from typing import List

from application.db.dataaccessobjects.links_dao import LinksDao


class DatabaseManager:
    """При создании объекта класса осуществиться подключение к бд или создастся бд,
     затем проверка или создание таблицы LINKS"""

    def __init__(self):
        self.__db = sqlite3.connect(r'application\db\cian.db')  # ссылка на файл бд
        LinksDao.init_table(self.__db)

    def insert_link_into_links(self, link):
        """Сохранение ссылки в таблицу links"""
        try:
            LinksDao.insert(self.__db, link)
        except Exception as err:
            pass

    def get_links_from_db(self) -> List[str]:
        """Получение всех ссылок из БД"""
        return LinksDao.select_all_links(self.__db)
