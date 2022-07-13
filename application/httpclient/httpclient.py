from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HttpClient:
    def __init__(self):
        self._ua = UserAgent()

    # где нужен wait?
    def get_page_source(self, link: str) -> str:
        """Получение html разметки страницы"""
        path = r'C:\Program Files (x86)\chromedriver.exe'
        options = Options()
        user_agent = self._ua.random
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        driver.maximize_window()
        driver.get(link)
        return driver.page_source
