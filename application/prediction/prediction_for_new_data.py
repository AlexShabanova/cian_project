import locale
import pickle
import sqlite3

import pandas as pd

from application.prediction.generation_df_for_model import generate_df_for_model
from application.prediction.prediction_data_models import InteriorDesign, HouseType, Bathroom, \
    HousingType, Seller, CeilingHeight, District, BuiltYear, Mortgage, SaleType, Rooms, FlatType, Heating, Parking, \
    SuspiciousFlat


def predict_price_for_new_data(
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
) -> str:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    conn = sqlite3.connect('db\cian.db')

    df = pd.read_sql_query('''
                                   SELECT *
                                   FROM ad_data_cleaned_with_fixed_age
                                   ''', conn)
    df.drop('price', axis=1, inplace=True)
    new_data_df = generate_df_for_model(
        flat_type,
        rooms,
        sale_type,
        mortgage,
        area,
        living_area,
        kitchen_area,
        floor,
        floors,
        built_year,
        district,
        ceiling_height,
        heating,
        parking,
        metro_station,
        seller,
        housing_type,
        bathroom,
        house_type,
        is_suspicious,
        interior_design
    )
    df_with_new_ad = pd.concat([df, new_data_df], ignore_index=True)
    categorical_columns = df_with_new_ad.select_dtypes(include=['object']).columns
    df_with_new_ad_dummies = pd.get_dummies(df_with_new_ad, columns=categorical_columns)
    # Select last row of the dataframe as a dataframe object
    new_ad_last_row = df_with_new_ad_dummies.iloc[-1:]
    # загрузка/десериализация модели
    loaded_rf_model = pickle.load(open('fitted_models/rf_model.pkl', 'rb'))
    # предсказание на новых данных
    result = loaded_rf_model.predict(new_ad_last_row)
    # отформатированный результат
    return locale.currency(result, grouping=True).replace(u'\xa0', ' ')
