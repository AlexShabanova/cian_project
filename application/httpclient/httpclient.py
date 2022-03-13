import requests as requests
from fake_useragent import UserAgent

from application.datamodel.data_models import Result, Success, Error


class HttpClient:
    def __init__(self):
        self._ua = UserAgent()

    def request(self, url: str) -> Result:
        try:
            header = {'user-agent': self._ua.random}
            response = requests.get(url, headers=header).text
            return Success(response)
        except Exception as err:
            return Error(err)
