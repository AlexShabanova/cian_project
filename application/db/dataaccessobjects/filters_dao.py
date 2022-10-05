from sqlite3 import Connection
from typing import List


class FiltersDao:
    """Хранит порядковые номера фильтров, по которому все выгружено"""

    @staticmethod
    def init_filters_table(db: Connection):
        """Создание таблицы ссылок на объявления"""
        query = """
        CREATE TABLE IF NOT EXISTS filters (
            filter INTEGER UNIQUE NOT NULL PRIMARY KEY
        );
        """
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def insert_processed_filter(db: Connection, processed_filter):
        """Заполнение таблицы"""
        query = f"INSERT INTO filters (filter)  VALUES ('{processed_filter}');"
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def get_all_processed_filters(db: Connection) -> List[int]:
        """Получение списка номеров фильтров, по которым все выгружено"""
        query = """SELECT filter FROM filters"""
        cursor = db.cursor()
        cursor.execute(query)
        filters_list_of_tuples = cursor.fetchall()
        filters_list = [f for t in filters_list_of_tuples for f in t]
        cursor.close()
        return filters_list
