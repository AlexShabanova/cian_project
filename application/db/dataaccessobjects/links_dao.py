from sqlite3 import Connection


class LinksDao:
    """Хранит все запросы для работы с ссылками с главной страницы"""

    @staticmethod
    def init_table(db: Connection):
        """Создание таблицы"""
        query = """
        CREATE TABLE IF NOT EXISTS LINKS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            is_processed INTEGER NOT NULL
        );
        """  # Запрос на создание таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def insert(db: Connection, id, link):
        """Заполнение таблицы"""
        query = f"INSERT INTO LINKS (id, link, is_processed)  VALUES ({id}, '{link}', 0);"  # Запрос на заполнение таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()


