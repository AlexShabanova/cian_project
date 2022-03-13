from application.datamodel.data_models import DealType, OfferType, Region, Success, Error
from application.httpclient.httpclient import HttpClient


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region
        self.test()

    def test(self):
        client = HttpClient()
        result = client.request(
            'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&object_type%5B0%5D=1&offer_type=flat&p=8&region=1&room1=1&room2=1')
        if isinstance(result, Success):
            print(result.data)
        elif isinstance(result, Error):
            print(result.exception)
