from application.datamodel.data_models import DealType, OfferType, Region, Success, Error
from application.db.database_manager import DatabaseManager
from application.httpclient.httpclient import HttpClient
from application.parsers.main_page_parser import MainPageParser
import time


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        self.manager = DatabaseManager()
        self.client = HttpClient()

    def get_links_main_page(self):
        """Получение списка ссылок на объявления с главной страницы
        Обработка ошибок: если приходит пустой лист, лист None, конец номеров страниц, ссылка есть в бд """
        page_number = 1
        last_page = False
        while not last_page:
            print(f"Текущий номер страницы: {page_number}")
            link = f'https://www.cian.ru/cat.php?deal_type={self.deal_type.value}&engine_version=2&offer_type={self.offer_type.value}&p={page_number}&region={self.region.value}'
            print(link)
            http_page = self.client.request(link)
            if isinstance(http_page, Success):
                print(http_page.data)
                links_from_main_page = MainPageParser.parse_links_from_main_page(http_page.data)
                print(links_from_main_page)
                links_from_db = self.manager.get_links_from_db()
                check = all(link in links_from_db for link in links_from_main_page)
                if check is True:
                    last_page = True
                else:
                    for link in links_from_main_page:
                        self.manager.insert_link_into_links(link)
                    time.sleep(5)
                    page_number += 1
                if 'captcha' in http_page.data:
                    time.sleep(300)
                    last_page = True
            else:
                break
        print('Закончили получать ссылки с главной страницы')
