from application.datamodel.data_models import DealType, OfferType, Region, Success, Error
from application.db.database_manager import DatabaseManager
from application.httpclient.httpclient import HttpClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        self.manager = DatabaseManager()
        self.client = HttpClient()

    def get_links_from_page(self):
        """Получение списка ссылок на объявления с главной страницы
        Обработка ошибок: если приходит пустой лист, лист None, конец номеров страниц, ссылка есть в бд """
        page_number = 1
        last_page = False
        path = r'C:\Program Files (x86)\chromedriver.exe'
        driver = webdriver.Chrome(path)
        driver.maximize_window()
        try:
            while last_page is False:
                print(f"Текущий номер страницы: {page_number}")
                link = f'https://www.cian.ru/cat.php?deal_type={self.deal_type.value}&engine_version=2&offer_type={self.offer_type.value}&p={page_number}&region={self.region.value}'
                print(link)
                driver.get(link)
                links_from_page = []
                try:
                    components = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//article[@data-name='CardComponent']/*")))
                    for elem in components:
                        try:
                            link = elem.find_element(by=By.TAG_NAME, value='a')
                            links_from_page.append(link.get_attribute('href'))
                        except Exception as err:
                            pass
                    print(f"результат: {links_from_page}")
                    links_from_db = self.manager.get_links_from_db()
                    check = all(link in links_from_db for link in links_from_page)
                    if check is True:
                        last_page = True
                    else:
                        for l in links_from_page:
                            self.manager.insert_link_into_links(l)
                        time.sleep(5)
                        page_number += 1
                    if 'captcha' in driver.page_source:
                        time.sleep(300)
                        last_page = True

                except Exception as err:
                        pass
        finally:
            driver.quit()

        print('Закончили получать ссылки со страниц')
