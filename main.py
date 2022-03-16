from application.Application import Application
from application.datamodel.data_models import DealType, OfferType, Region
from application.db.database_manager import DatabaseManager

if __name__ == '__main__':
    Application(deal_type=DealType.sale, offer_type=OfferType.flat, region=Region.moscow)


