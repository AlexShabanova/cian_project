import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HttpClient:
    def __init__(self):
        self._ua = UserAgent()
        options = Options()
        path = r'C:\Program Files (x86)\chromedriver.exe'
        user_agent = self._ua.random
        options.add_argument(f'user-agent={user_agent}')
        self._driver = webdriver.Chrome(chrome_options=options, executable_path=path)

    def get_page_source(self, link: str) -> str:
        """Получение html разметки страницы"""
        # path = r'C:\Program Files (x86)\chromedriver.exe'
        # options = Options()
        # user_agent = self._ua.random
        # options.add_argument(f'user-agent={user_agent}')  # fixme если что вынести в init
        # driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        # driver.maximize_window()
        self._driver.get(link)
        while 'Таак, что-то страница не загрузилась...' in self._driver.page_source:
            time.sleep(5)
            print("Не загрузилась страница")
            self._driver.get(link)
        time.sleep(4)
        return self._driver.page_source
