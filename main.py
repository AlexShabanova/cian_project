from application.Application import Application
from application.datamodel.data_models import DealType, OfferType, Region

if __name__ == '__main__':
    app = Application(deal_type=DealType.sale, offer_type=OfferType.flat, region=Region.moscow)
    app.get_links_main_page()
