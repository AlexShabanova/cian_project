from itertools import product

from application.Application import Application
from application.datamodel.data_models import DealType, OfferType, Region, ObjectType, RoomType

if __name__ == '__main__':

    price_range_min = [x for x in range(1_000_001, 1_000_000_000, 500_000)]
    price_range_max = [x for x in range(1_500_000, 1_000_000_001, 500_000)]
    price_ranges = [(min_price, max_price) for min_price, max_price in zip(price_range_min, price_range_max)]
    variants = [
        [e for e in ObjectType],
        [e for e in RoomType],
        price_ranges
    ]
    all_parameters = list(product(*variants))

    app: Application
    for parameters in all_parameters:
        object_type = parameters[0]
        room_type = parameters[1]
        min_price = parameters[2][0]
        max_price = parameters[2][1]
        app = Application(
            deal_type=DealType.sale,
            offer_type=OfferType.flat,
            region=Region.moscow,
            object_type=object_type,
            room=room_type,
            minprice=min_price,
            maxprice=max_price
        )
        app.get_links_from_page()
    # app.get_ad_data_from_all_links()
    # app.generate_fake_ad_data(10_000)
    # app.update_incorrect_values()
