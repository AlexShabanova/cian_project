from application.datamodel.data_models import DealType, OfferType, Region, Success, Error
from application.httpclient.httpclient import HttpClient
from application.parsers.main_page_parser import MainPageParser


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        # self.test()

    def test(self):
        client = HttpClient()
        result = client.request(
            'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=2&region=1')
        if isinstance(result, Success):
            print(result.data)
        elif isinstance(result, Error):
            print(result.exception)

    def get_links_main_page(self):
        """Получение списка ссылок на объявления с главной страницы
        Обработка ошибок: если приходит пустой лист, лист None, конец номеров страниц, ссылка есть в бд """
        page_number = 1
        client = HttpClient()
        while True:
            link = f'https://www.cian.ru/cat.php?deal_type={self.deal_type.value}&engine_version=2&offer_type={self.offer_type.value}&p={page_number}&region={self.region.value}'
            print(link)
            http_page = client.request(link)
            if isinstance(http_page, Success):
                links_from_main_page = MainPageParser.parse_links_from_main_page(http_page.data)
                print(links_from_main_page)
                page_number += 1
            else:
                break
