from sqlite3 import Connection
from typing import List


class LinksDao:
    """Хранит все запросы для работы с ссылками с главной страницы"""

    @staticmethod
    def init_links_table(db: Connection):
        """Создание таблицы ссылок на объявления"""
        query = """
        CREATE TABLE IF NOT EXISTS links (
            link TEXT UNIQUE NOT NULL PRIMARY KEY,
            is_processed INTEGER NOT NULL
        );
        """  # Запрос на создание таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def insert_link(db: Connection, link):
        """Заполнение таблицы"""
        query = f"INSERT INTO links (link, is_processed)  VALUES ('{link}', 0);"  # Запрос на заполнение таблицы
        cursor = db.cursor()
        cursor.execute(query) #  sqlite3.IntegrityError: UNIQUE constraint failed: links.link при повторной ссылке
        db.commit()
        cursor.close()

    @staticmethod
    def set_link_processed(db: Connection, link):
        """Обновление is_processed = true когда скачаны данные по объявлению"""
        query = f"UPDATE links SET is_processed = 1 WHERE link = '{link}'"
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def select_all_unprocessed_links(db: Connection) -> List[str]:
        """Запрос на вывод всех ссылок из БД"""
        query = """SELECT link FROM links WHERE is_processed = 0"""
        cursor = db.cursor()
        cursor.execute(query)
        links_list_of_tuples = cursor.fetchall()
        links_list = [link for t in links_list_of_tuples for link in t]
        cursor.close()
        return links_list
