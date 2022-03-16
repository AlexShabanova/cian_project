import sqlite3

from application.db.dataaccessobjects.links_dao import LinksDao


class DatabaseManager:
    """При создании объекта класса осуществиться подключение к бд или создастся бд,
     затем проверка или создание таблицы LINKS"""

    def __init__(self):
        self.__db = sqlite3.connect(r'application\db\cian.db')  # ссылка на файл бд
        LinksDao.init_table(self.__db)

    def insert_link_into_links(self, id, link):
        LinksDao.insert(self.__db, id, link)
