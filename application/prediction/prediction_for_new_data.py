import locale
import pickle
import sqlite3

import pandas as pd

from application.prediction.generation_df_for_model import generate_df_for_model
from application.prediction.prediction_data_models import InteriorDesign, HouseType, Bathroom, \
    HousingType, Seller, CeilingHeight, District, BuiltYear, Mortgage, SaleType, Rooms, FlatType

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

conn = sqlite3.connect('..\db\cian.db')

df = pd.read_sql_query('''
                               SELECT *
                               FROM ad_data_cleaned_with_fixed_age
                               ''', conn)
df.drop('price', axis=1, inplace=True)
build_year = BuiltYear()
build_year.year = 2004
ceiling_height = CeilingHeight()
ceiling_height.height = 2.64
new_data_df = generate_df_for_model(flat_type=FlatType.flat, rooms=Rooms.one, sale_type=SaleType.free_sale,
                                    mortgage=Mortgage.mortgage_true, area=39.0, kitchen_area=9.0, living_area=19.0,
                                    floor=5, floors=10, built_year=build_year, district=District.ZAO,
                                    metro_station='Фили',
                                    ceiling_height=ceiling_height, seller=Seller.owner,
                                    housing_type=HousingType.second_built,
                                    house_type=HouseType.panel, bathroom=Bathroom.separate_1_wc,
                                    interior_design=InteriorDesign.cosmetic
                                    )
df_with_new_ad = pd.concat([df, new_data_df], ignore_index=True)
categorical_columns = df_with_new_ad.select_dtypes(include=['object']).columns
df_with_new_ad_dummies = pd.get_dummies(df_with_new_ad, columns=categorical_columns)
# Select last row of the dataframe as a dataframe object
new_ad_last_row = df_with_new_ad_dummies.iloc[-1:]
# загрузка/десериализация модели
loaded_rf_model = pickle.load(open('../fitted_models/rf_model.pkl', 'rb'))
# предсказание на новых данных
result = loaded_rf_model.predict(new_ad_last_row)
# отформатированный результат
print(locale.currency(result, grouping=True).replace(u'\xa0', ' '))
