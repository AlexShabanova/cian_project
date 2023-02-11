from datetime import date

import pandas as pd

from application.prediction.prediction_data_models import InteriorDesign, SuspiciousFlat, HouseType, Bathroom, \
    HousingType, Seller, Parking, Heating, CeilingHeight, District, BuiltYear, Mortgage, SaleType, Rooms, FlatType


def generate_df_for_model(
        flat_type: FlatType,
        rooms: Rooms,
        sale_type: SaleType,
        mortgage: Mortgage,
        area: float,
        living_area: float,
        kitchen_area: float,
        floor: int,
        floors: int,
        built_year: BuiltYear,
        district: District,
        ceiling_height: CeilingHeight,
        heating: Heating = Heating.centralized,
        parking: Parking = Parking.spontaneous,
        metro_station: str = 'пропущено',
        seller: Seller = Seller.not_mentioned,
        housing_type: HousingType = HousingType.missing,
        bathroom: Bathroom = Bathroom.missing,
        house_type: HouseType = HouseType.missing,
        is_suspicious: SuspiciousFlat = SuspiciousFlat.not_suspicious,
        interior_design: InteriorDesign = InteriorDesign.missing
) -> pd.DataFrame:
    data_dict = {'flat_type': flat_type.value, 'rooms': rooms.value, 'sale_type': sale_type.value,
                 'mortgage': mortgage.value, 'area': area,
                 'living_area': living_area, 'kitchen_area': kitchen_area, 'floor': floor, 'floors': floors,
                 'property_age': date.today().year - int(built_year.year),
                 'district': district.value, 'metro_station': metro_station, 'seller': seller.value,
                 'housing_type': housing_type.value,
                 'ceiling_height': ceiling_height.height, 'bathroom': bathroom.value, 'house_type': house_type.value,
                 'parking': parking.value,
                 'heating': heating.value,
                 'is_suspicious': is_suspicious.value, 'interior_design': interior_design.value}

    return pd.DataFrame(data=data_dict, index=[0])
