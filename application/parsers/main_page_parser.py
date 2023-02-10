from typing import List

from bs4 import BeautifulSoup


class MainPageParser:

    @staticmethod
    def parse_links_from_main_page(page_source: str) -> List[str]:
        """Получает url страницы и отдает список ссылок на объявления"""
        soup = BeautifulSoup(page_source, 'lxml')
        card_components = soup.find_all('article', {'data-name': 'CardComponent'})
        return [component.find('a').get('href') for component in card_components]
