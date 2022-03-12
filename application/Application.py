from application.datamodel.data_models import DealType, OfferType, Region


class Application:

    def __init__(self, deal_type: DealType, offer_type: OfferType, region: Region):
        self.deal_type = deal_type
        self.offer_type = offer_type
        self.region = region


