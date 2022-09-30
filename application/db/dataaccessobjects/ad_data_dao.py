from sqlite3 import Connection


class AdDataDao:
    """Хранит все запросы для работы с данными объявлений"""

    @staticmethod
    def init_ads_table(db: Connection):
        """Создание таблицы с данными из объявления"""
        query = """
        CREATE TABLE IF NOT EXISTS ad_data (
            link TEXT UNIQUE NOT NULL PRIMARY KEY,
            flat_type TEXT,
            rooms INTEGER,
            price INTEGER,
            sale_type TEXT,
            mortgage INTEGER,
            area REAL,
            living_area REAL,
            kitchen_area REAL,
            floor INTEGER,
            floors INTEGER,
            built_year INTEGER,
            address TEXT,
            district TEXT,
            metro_station TEXT,
            seller TEXT,
            housing_type TEXT,
            planning TEXT,
            ceiling_height REAL,
            bathroom TEXT,
            balcony_loggia TEXT,
            repair TEXT,
            view TEXT,
            finished_shell_condition TEXT,
            house_type TEXT,
            house_class TEXT,
            building_number INTEGER,
            parking TEXT,
            elevators TEXT,
            housing_line TEXT,
            floor_type TEXT,
            entrance_number INTEGER,
            heating TEXT,
            unsafe_house TEXT,
            garbage_disposal TEXT,
            gas_supply TEXT,
            description_text TEXT
        );
        """  # Запрос на создание таблицы
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    @staticmethod
    def insert_ad_data(db: Connection, link, flat_type, rooms, price, sale_type, mortgage, area,
                       living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller,
                       housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                       finished_shell_condition, house_type, house_class, building_number, parking, elevators,
                       housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply,
                       description_text):
        """Заполнение таблицы"""
        cursor = db.cursor()
        cursor.execute("""INSERT INTO ad_data (link, flat_type, rooms, price, sale_type, mortgage, area, living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition, house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply, description_text) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (link, flat_type, rooms, price, sale_type, mortgage, area, living_area, kitchen_area, floor, floors, built_year, address, district, metro_station, seller, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition, house_type, house_class, building_number, parking, elevators, housing_line, floor_type, entrance_number, heating, unsafe_house, garbage_disposal, gas_supply, description_text))
        db.commit()
        cursor.close()

    @staticmethod
    def change_column_values(db: Connection):
        cursor = db.cursor()
        cursor.execute("""update ad_data set building_number = (select (abs(rooms-10)))""")
        db.commit()
        cursor.close()
