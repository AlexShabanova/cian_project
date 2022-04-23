from sqlite3 import Connection
from typing import List


class LinksDao:
    """Хранит все запросы для работы с ссылками с главной страницы"""

    @staticmethod
    def init_table(db: Connection):
        """Создание таблицы"""
        query = """
        CREATE TABLE IF NOT EXISTS links (
            link TEXT NOT NULL PRIMARY KEY,
            is_processed INTEGER NOT NULL
        );
        """  # Запрос на создание таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def insert(db: Connection, link):
        """Заполнение таблицы"""
        query = f"INSERT INTO LINKS (link, is_processed)  VALUES ('{link}', 0);"  # Запрос на заполнение таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def select_all_links(db: Connection) -> List[str]:
        """Запрос на вывод всех ссылок из БД"""
        query = """SELECT link FROM links"""
        cursor = db.cursor()
        cursor.execute(query)
        links_list_of_tuples = cursor.fetchall()
        links_list = [link for t in links_list_of_tuples for link in t]
        cursor.close()
        return links_list


