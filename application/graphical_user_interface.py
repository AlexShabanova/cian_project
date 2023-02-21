import tkinter
from tkinter import END

import customtkinter

from application.prediction.prediction_data_models import InteriorDesign, HouseType, Bathroom, \
    Seller, Parking, Heating, CeilingHeight, District, BuiltYear, SaleType, Rooms, FlatType, Mortgage, SuspiciousFlat, \
    HousingType
from application.prediction.prediction_for_new_data import predict_price_for_new_data

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUIApp(customtkinter.CTk):
    WIDTH = 1000
    HEIGHT = 700

    def __init__(self):
        super().__init__()

        self.geometry(f"{GUIApp.WIDTH}x{GUIApp.HEIGHT}")
        self.title("Стоимость квартиры в Москве")
        self.protocol()
        self.minsize(300, 200)

        # create 4x3 grid system
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2, 3), weight=0)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)

        # create first frame with widgets
        self.frame_1 = customtkinter.CTkFrame(self)
        self.frame_1.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # self.frame_1.grid_rowconfigure(3, weight=1)

        # FlatType
        self.radio_var_flat_type = tkinter.StringVar(value="квартира")
        self.flat_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип недвижимости:",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.flat_type_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_1, text="квартира",
                                                           variable=self.radio_var_flat_type,
                                                           value="квартира", font=("Roboto", 12))
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_1, text="апартаменты",
                                                           variable=self.radio_var_flat_type,
                                                           value="апартаменты", font=("Roboto", 12))
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.radio_var_housing_type = tkinter.StringVar(value=0)
        self.housing_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип жилья:",
                                                         font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.housing_type_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_1, text="вторичное",
                                                           variable=self.radio_var_housing_type,
                                                           value="вторичное", font=("Roboto", 14))
        self.radio_button_3.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.frame_1, text="новостройка",
                                                           variable=self.radio_var_housing_type,
                                                           value="новостройка", font=("Roboto", 14))
        self.radio_button_4.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        self.radio_var_housing_type.set("вторичное")

        self.checkbox_mortgage = customtkinter.CTkCheckBox(master=self.frame_1, text="Ипотека",
                                                           font=customtkinter.CTkFont(size=14, weight="bold"))
        self.checkbox_mortgage.grid(row=6, column=0, pady=(20, 10), padx=20, sticky="w")

        self.sale_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип продажи:",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.sale_type_label.grid(row=7, column=0, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_sale_type = customtkinter.CTkOptionMenu(self.frame_1, dynamic_resizing=False, width=200,
                                                                 values=[e.value for e in SaleType])
        self.option_menu_sale_type.grid(row=8, column=0, padx=20, pady=(5, 10))
        self.option_menu_sale_type.set("свободная продажа")

        self.seller_label = customtkinter.CTkLabel(self.frame_1, text="Продавец:",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.seller_label.grid(row=9, column=0, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_seller = customtkinter.CTkOptionMenu(self.frame_1, dynamic_resizing=False, width=200,
                                                              values=[e.value for e in Seller])
        self.option_menu_seller.grid(row=10, column=0, padx=20, pady=(5, 10))
        self.option_menu_seller.set("не указано")

        # create second frame with widgets
        self.frame_2 = customtkinter.CTkFrame(self, width=300)  # width=100
        self.frame_2.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.rooms_label = customtkinter.CTkLabel(self.frame_2, text="Комнатность:",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.rooms_label.grid(row=1, column=1, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_rooms = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=200,
                                                             values=["-1", "0", "1", "2", "3", "4", "5", "6"])
        self.option_menu_rooms.grid(row=2, column=1, padx=20, pady=(5, 5), sticky="w")
        self.rooms_comment_label = customtkinter.CTkLabel(self.frame_2,
                                                          text="-1: свободная планировка\n 0: квартира-студия",
                                                          font=customtkinter.CTkFont(size=12),
                                                          anchor="w", justify="left")
        self.rooms_comment_label.grid(row=3, column=1, padx=20, pady=(10, 5), sticky="nw")
        self.area_label = customtkinter.CTkLabel(self.frame_2, text="Общая площадь:",
                                                 font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.area_label.grid(row=4, column=1, padx=20, pady=(15, 5), sticky="w")
        self.entry_area = customtkinter.CTkEntry(self.frame_2, width=150, placeholder_text="м\u00B2  (через . )")
        self.entry_area.grid(row=5, column=1, padx=(20, 0), pady=(10, 20), sticky="w")

        self.kitchen_area_label = customtkinter.CTkLabel(self.frame_2, text="Площадь кухни:",
                                                         font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.kitchen_area_label.grid(row=6, column=1, padx=20, pady=(10, 5), sticky="w")
        self.entry_kitchen_area = customtkinter.CTkEntry(self.frame_2, width=150,
                                                         placeholder_text="м\u00B2  (через . )")
        self.entry_kitchen_area.grid(row=7, column=1, padx=(20, 0), pady=(10, 20), sticky="w")

        self.living_area_label = customtkinter.CTkLabel(self.frame_2, text="Жилая площадь:",
                                                        font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.living_area_label.grid(row=8, column=1, padx=20, pady=(10, 5), sticky="w")
        self.entry_living_area = customtkinter.CTkEntry(self.frame_2, width=150, placeholder_text="м\u00B2  (через . )")
        self.entry_living_area.grid(row=9, column=1, padx=(20, 0), pady=(5, 20), sticky="w")
        self.bathroom_label = customtkinter.CTkLabel(self.frame_2, text="Санузел:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.bathroom_label.grid(row=10, column=1, padx=20, pady=(10, 5), sticky="w")
        self.option_menu_bathroom = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=230,
                                                                values=[e.value for e in Bathroom])
        self.option_menu_bathroom.grid(row=11, column=1, padx=20, pady=(5, 10))
        self.option_menu_bathroom.set("пропущено")
        self.bathroom_label = customtkinter.CTkLabel(self.frame_2, text="Ремонт:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.bathroom_label.grid(row=12, column=1, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_interior_design = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=230,
                                                                       values=[e.value for e in InteriorDesign])
        self.option_menu_interior_design.grid(row=13, column=1, padx=20, pady=(5, 10))
        self.option_menu_interior_design.set("пропущено")

        # create third frame with widgets
        self.frame_3 = customtkinter.CTkFrame(self, width=250)
        self.frame_3.grid(row=0, column=2, rowspan=1, sticky="nsew")
        self.floor_label = customtkinter.CTkLabel(self.frame_3, text="Этаж:",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.floor_label.grid(row=1, column=2, padx=20, pady=(20, 5), sticky="w")
        self.entry_floor = customtkinter.CTkEntry(self.frame_3, width=100)
        self.entry_floor.grid(row=2, column=2, padx=(20, 0), pady=(10, 20), sticky="w")
        self.floors_label = customtkinter.CTkLabel(self.frame_3, text="Всего этажей:",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.floors_label.grid(row=3, column=2, padx=20, pady=(15, 5), sticky="w")
        self.entry_floors = customtkinter.CTkEntry(self.frame_3, width=100)
        self.entry_floors.grid(row=4, column=2, padx=(20, 0), pady=(10, 20), sticky="w")
        self.built_year_label = customtkinter.CTkLabel(self.frame_3, text="Год постройки:",
                                                       font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.built_year_label.grid(row=5, column=2, padx=20, pady=(15, 5), sticky="w")
        self.entry_built_year = customtkinter.CTkEntry(self.frame_3, width=100)
        self.entry_built_year.grid(row=6, column=2, padx=(20, 0), pady=(10, 20), sticky="w")
        self.ceiling_height_label = customtkinter.CTkLabel(self.frame_3, text="Высота потолков:",
                                                           font=customtkinter.CTkFont(size=16, weight="bold"),
                                                           anchor="w")
        self.ceiling_height_label.grid(row=7, column=2, padx=20, pady=(15, 5), sticky="w")
        self.entry_ceiling_height = customtkinter.CTkEntry(self.frame_3, width=150, placeholder_text="м  (через . )")
        self.entry_ceiling_height.grid(row=8, column=2, padx=(20, 0), pady=(10, 20), sticky="w")

        # create fourth frame with widgets
        self.frame_4 = customtkinter.CTkFrame(self)
        self.frame_4.grid(row=1, column=2, rowspan=1, sticky="nsew")
        self.district_label = customtkinter.CTkLabel(self.frame_4, text="Район:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.district_label.grid(row=2, column=2, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_district = customtkinter.CTkOptionMenu(self.frame_4, dynamic_resizing=False, width=150,
                                                                values=[e.value for e in District])
        self.option_menu_district.grid(row=3, column=2, padx=20, pady=(5, 10), sticky="w")
        self.metro_label = customtkinter.CTkLabel(self.frame_4, text="Метро:",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"),
                                                  anchor="w")
        self.metro_label.grid(row=4, column=2, padx=20, pady=(15, 5), sticky="w")
        self.entry_metro = customtkinter.CTkEntry(self.frame_4, width=200, placeholder_text=" с заглавной буквы")
        self.entry_metro.grid(row=5, column=2, padx=(20, 10), pady=(10, 20), sticky="w")

        # create fifth frame with widgets
        self.frame_5 = customtkinter.CTkFrame(self)
        self.frame_5.grid(row=0, column=3, rowspan=2, sticky="nsew")
        self.house_type_label = customtkinter.CTkLabel(self.frame_5, text="Тип дома:",
                                                       font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.house_type_label.grid(row=1, column=3, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_house_type = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                                  values=[e.value for e in HouseType])
        self.option_menu_house_type.grid(row=2, column=3, padx=20, pady=(5, 15))
        self.option_menu_house_type.set("пропущено")
        self.parking_label = customtkinter.CTkLabel(self.frame_5, text="Парковка:",
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.parking_label.grid(row=3, column=3, padx=20, pady=(20, 10), sticky="w")
        self.option_menu_parking = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                               values=[e.value for e in Parking])
        self.option_menu_parking.grid(row=4, column=3, padx=20, pady=(5, 20))
        self.option_menu_parking.set("стихийная")
        self.heating_label = customtkinter.CTkLabel(self.frame_5, text="Отопление:",
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.heating_label.grid(row=5, column=3, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_heating = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                               values=[e.value for e in Heating])
        self.option_menu_heating.grid(row=6, column=3, padx=20, pady=(5, 20))
        self.option_menu_heating.set("центральное")
        self.checkbox_suspicious = customtkinter.CTkCheckBox(master=self.frame_5, text="Подозрительная\nквартира",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.checkbox_suspicious.grid(row=7, column=3, pady=(35, 10), padx=20, sticky="w")

        # create appearance mode frame with widgets
        self.appearance_mode_frame = customtkinter.CTkFrame(self)
        self.appearance_mode_frame.grid(row=2, column=0, rowspan=1, sticky="nsew")
        self.appearance_mode_frame.grid_rowconfigure(2, weight=0)
        self.appearance_mode_label = customtkinter.CTkLabel(self.appearance_mode_frame,
                                                            font=customtkinter.CTkFont(size=14),
                                                            text="Цветовая схема:",
                                                            anchor="s")
        self.appearance_mode_label.grid(row=3, column=0, padx=(20, 20), pady=(10, 0), sticky="s")
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.appearance_mode_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 10), sticky="s")

        # create main entry
        self.entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16, weight="bold"), )
        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # create main button
        self.main_button_1 = customtkinter.CTkButton(master=self, text="РАССЧИТАТЬ", fg_color="transparent",
                                                     border_width=2,
                                                     font=customtkinter.CTkFont(size=14, weight="bold"),
                                                     text_color=("gray10", "#DCE4EE"), command=self.calculate_price)
        self.main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def calculate_price(self):
        built_year = BuiltYear()
        built_year.year = int(self.entry_built_year.get())

        ceiling_height = CeilingHeight()
        ceiling_height.height = (float(self.entry_ceiling_height.get()))

        flat_type = FlatType(self.radio_var_flat_type.get())
        rooms = Rooms(int(self.option_menu_rooms.get()))
        sale_type = SaleType(self.option_menu_sale_type.get())
        mortgage = Mortgage(self.checkbox_mortgage.get())
        area = float(self.entry_area.get())
        living_area = float(self.entry_living_area.get())
        kitchen_area = float(self.entry_kitchen_area.get())
        floor = int(self.entry_floor.get())
        floors = int(self.entry_floors.get())
        district = District(self.option_menu_district.get())
        heating = Heating(self.option_menu_heating.get())
        parking = Parking(self.option_menu_parking.get())
        metro_station = self.entry_metro.get()
        seller = Seller(self.option_menu_seller.get())
        housing_type = HousingType(self.radio_var_housing_type.get())
        bathroom = Bathroom(self.option_menu_bathroom.get())
        house_type = HouseType(self.option_menu_house_type.get())
        is_suspicious = SuspiciousFlat(self.checkbox_suspicious.get())
        interior_design = InteriorDesign(self.option_menu_interior_design.get())
        print(flat_type,
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
              interior_design)

        self.entry.configure(state='normal')
        self.entry.delete(0, END)
        result = predict_price_for_new_data(flat_type,
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
                                            interior_design)
        self.entry.insert(0, result)
        self.entry.configure(state='disabled')

app = GUIApp()
app.mainloop()
