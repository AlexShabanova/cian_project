from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from bs4 import BeautifulSoup
import lxml


# class MainPageParser:
#
#     @staticmethod
#     def parse_links_from_main_page(url: str) -> List[str]:
#         """получает url страницы и отдает список ссылок на объявления"""
#         # soup = BeautifulSoup(page, 'lxml')
#         # card_components = soup.find_all('article', {'data-name': 'CardComponent'})
#         # return [component.find('a').get('href') for component in card_components]
