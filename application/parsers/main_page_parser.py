from typing import List

from bs4 import BeautifulSoup
import lxml


class MainPageParser:

    @staticmethod
    def parse_links_from_main_page(page: str) -> List[str]:
        """получает всю страницу и отдает список ссылок на объявления"""
        soup = BeautifulSoup(page, 'lxml')
        card_components = soup.find_all('article', {'data-name': 'CardComponent'})
        return [component.find('a').get('href') for component in card_components]