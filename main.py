from itertools import product
from typing import List, Tuple

from application.Application import Application
from application.datamodel.data_models import DealType, OfferType, Region, ObjectType, RoomType
from application.db.database_manager import DatabaseManager


def generate_filters() -> Tuple[List]:
    processed_filters = db_manager.get_all_processed_filters()

    price_range_min = [x for x in range(1_000_001, 1_000_000_000, 500_000)]
    price_range_max = [x for x in range(1_500_000, 1_000_000_001, 500_000)]
    price_ranges = [(min_price, max_price) for min_price, max_price in zip(price_range_min, price_range_max)]
    variants = [
        [e for e in ObjectType],
        [e for e in RoomType],
        price_ranges
    ]
    all_parameters = list(product(*variants))
    return processed_filters, all_parameters


def skip_empty_pages(all_parameters: List[Tuple[int]]):
    """Пропуск заведомо пустых страниц"""
    test = []
    for index, filter in enumerate(all_parameters):
        object_type = filter[0]
        room_type = filter[1]
        min_price = filter[2][0]
        max_price = filter[2][1]
        if object_type == ObjectType.secondary_build and room_type == RoomType.room9 and min_price >= 7_000_001:
            test.append(filter)
            print(index)
            db_manager.insert_processed_filter(index)
    app = Application(
        deal_type=DealType.sale,
        db_manager=db_manager,
        offer_type=OfferType.flat,
        region=Region.moscow,
        object_type=ObjectType.secondary_build,
        room=RoomType.room9,
        minprice=7_000_001,
        maxprice=1_000_000_000
    )
    app.get_links_from_page()


def get_links_with_current_filter(all_parameters: List[Tuple[int]], processed_filters: List[int]):
    for filter_index, parameters in enumerate(all_parameters):
        if filter_index in processed_filters:
            continue
        object_type = parameters[0]
        room_type = parameters[1]
        min_price = parameters[2][0]
        max_price = parameters[2][1]
        app = Application(
            deal_type=DealType.sale,
            db_manager=db_manager,
            offer_type=OfferType.flat,
            region=Region.moscow,
            object_type=object_type,
            room=room_type,
            minprice=min_price,
            maxprice=max_price
        )
        app.get_links_from_page()
        db_manager.insert_processed_filter(filter_index)
        print(f'Закончили получать ссылки по фильтру №{filter_index}: {parameters}')


if __name__ == '__main__':
    db_manager = DatabaseManager()

    app = Application(
        deal_type=DealType.sale,
        db_manager=db_manager,
        offer_type=OfferType.flat,
        region=Region.moscow,
        object_type=ObjectType.new_build,
        room=RoomType.room9,
        minprice=0,
        maxprice=0
    )
    # get_links_with_current_filter(generate_filters())
    # app.get_ad_data_from_all_links()
    app.parsing_ad_multiprocessing()
