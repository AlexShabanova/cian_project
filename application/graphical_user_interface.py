import tkinter

import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUIApp(customtkinter.CTk):
    # TODO настроить размеры экрана
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
        self.radio_var_flat_type = tkinter.StringVar(value=0)
        self.flat_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип недвижимости:",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.flat_type_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_1, text="квартира",
                                                           variable=self.radio_var_flat_type,
                                                           value=1, font=("Roboto", 12))
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_1, text="аппартаменты",
                                                           variable=self.radio_var_flat_type,
                                                           value=2, font=("Roboto", 12))
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.radio_var_housing_type = tkinter.StringVar(value=0)
        self.housing_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип жилья:",
                                                         font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.housing_type_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_1, text="вторичное",
                                                           variable=self.radio_var_housing_type,
                                                           value=1, font=("Roboto", 14))
        self.radio_button_3.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.frame_1, text="новостройка",
                                                           variable=self.radio_var_housing_type,
                                                           value=2, font=("Roboto", 14))
        self.radio_button_4.grid(row=5, column=0, pady=10, padx=20, sticky="w")

        self.checkbox_mortgage = customtkinter.CTkCheckBox(master=self.frame_1, text="Ипотека",
                                                           font=customtkinter.CTkFont(size=14, weight="bold"))
        self.checkbox_mortgage.grid(row=6, column=0, pady=(20, 10), padx=20, sticky="w")

        self.sale_type_label = customtkinter.CTkLabel(self.frame_1, text="Тип продажи:",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.sale_type_label.grid(row=7, column=0, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_sale_type = customtkinter.CTkOptionMenu(self.frame_1, dynamic_resizing=False, width=200,
                                                                 values=["свободная продажа", "альтернатива",
                                                                         "долевое участие (214-фз)"])
        self.option_menu_sale_type.grid(row=8, column=0, padx=20, pady=(5, 10))
        self.option_menu_sale_type.set("свободная продажа")

        self.seller_label = customtkinter.CTkLabel(self.frame_1, text="Продавец:",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.seller_label.grid(row=9, column=0, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_seller = customtkinter.CTkOptionMenu(self.frame_1, dynamic_resizing=False, width=200,
                                                              values=["агентство", "частный риелтор",
                                                                      "застройщик", "консультант", "собственник",
                                                                      "не указано"])
        self.option_menu_seller.grid(row=10, column=0, padx=20, pady=(5, 10))
        self.option_menu_seller.set("не указано")

        # create second frame with widgets
        self.frame_2 = customtkinter.CTkFrame(self, width=300)  # width=100
        self.frame_2.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.seller_label = customtkinter.CTkLabel(self.frame_2, text="Комнатность:",
                                                   font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.seller_label.grid(row=1, column=1, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_seller = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=200,
                                                              values=["1-комнатная", "2-комнатная",
                                                                      "3-комнатная", "4-комнатная", "5-комнатная",
                                                                      "6-комнатная", "студия", "свободная планировка"])
        self.option_menu_seller.grid(row=2, column=1, padx=20, pady=(5, 10), sticky="w")

        self.area_label = customtkinter.CTkLabel(self.frame_2, text="Общая площадь:",
                                                 font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.area_label.grid(row=3, column=1, padx=20, pady=(15, 5), sticky="w")
        self.entry_area = customtkinter.CTkEntry(self.frame_2, width=150, placeholder_text="м\u00B2")
        self.entry_area.grid(row=4, column=1, padx=(20, 0), pady=(10, 20), sticky="w")

        self.kitchen_area_label = customtkinter.CTkLabel(self.frame_2, text="Площадь кухни:",
                                                         font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.kitchen_area_label.grid(row=5, column=1, padx=20, pady=(10, 5), sticky="w")
        self.entry_kitchen_area = customtkinter.CTkEntry(self.frame_2, width=150, placeholder_text="м\u00B2")
        self.entry_kitchen_area.grid(row=6, column=1, padx=(20, 0), pady=(10, 20), sticky="w")

        self.living_area_label = customtkinter.CTkLabel(self.frame_2, text="Жилая площадь:",
                                                        font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.living_area_label.grid(row=7, column=1, padx=20, pady=(10, 5), sticky="w")
        self.entry_living_area = customtkinter.CTkEntry(self.frame_2, width=150, placeholder_text="м\u00B2")
        self.entry_living_area.grid(row=8, column=1, padx=(20, 0), pady=(5, 20), sticky="w")
        self.bathroom_label = customtkinter.CTkLabel(self.frame_2, text="Санузел:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.bathroom_label.grid(row=9, column=1, padx=20, pady=(10, 5), sticky="w")
        self.option_menu_bathroom = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=230,
                                                                values=["1 совмещенный", "1 раздельный",
                                                                        "1 совмещенный, 1 раздельный",
                                                                        "1 совмещенный, 2 раздельных",
                                                                        "1 совмещенный, 3 раздельных",
                                                                        "1 совмещенный, 4 раздельных", "2 совмещенных",
                                                                        "2 раздельных", "2 совмещенных, 1 раздельный",
                                                                        "2 совмещенных, 2 раздельных",
                                                                        "2 совмещенных, 3 раздельных",
                                                                        "2 совмещенных, 4 раздельных", "3 совмещенных",
                                                                        "3 раздельных",
                                                                        "3 совмещенных, 1 раздельный",
                                                                        "3 совмещенных, 2 раздельных",
                                                                        "3 совмещенных, 3 раздельных",
                                                                        "3 совмещенных, 4 раздельных", "4 совмещенных",
                                                                        "4 раздельных", "4 совмещенных, 1 раздельный",
                                                                        "4 совмещенных, 2 раздельных",
                                                                        "4 совмещенных, 3 раздельных",
                                                                        "4 совмещенных, 4 раздельных", "пропущено"])
        self.option_menu_bathroom.grid(row=10, column=1, padx=20, pady=(5, 10))
        self.option_menu_bathroom.set("пропущено")
        self.bathroom_label = customtkinter.CTkLabel(self.frame_2, text="Ремонт:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.bathroom_label.grid(row=11, column=1, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_bathroom = customtkinter.CTkOptionMenu(self.frame_2, dynamic_resizing=False, width=230,
                                                                values=["косметический",
                                                                        "без ремонта",
                                                                        "евроремонт",
                                                                        "чистовой",
                                                                        "дизайнерский",
                                                                        "черновой", "пропущено"])
        self.option_menu_bathroom.grid(row=12, column=1, padx=20, pady=(5, 10))
        self.option_menu_bathroom.set("пропущено")

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
        self.entry_ceiling_height = customtkinter.CTkEntry(self.frame_3, width=150, placeholder_text="м")
        self.entry_ceiling_height.grid(row=8, column=2, padx=(20, 0), pady=(10, 20), sticky="w")

        # create fourth frame with widgets
        self.frame_4 = customtkinter.CTkFrame(self)
        self.frame_4.grid(row=1, column=2, rowspan=1, sticky="nsew")
        self.district_label = customtkinter.CTkLabel(self.frame_4, text="Район:",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.district_label.grid(row=2, column=2, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_district = customtkinter.CTkOptionMenu(self.frame_4, dynamic_resizing=False, width=150,
                                                                values=["ЗелАО", "ТАО (Троицкий)", "САО", "ЮАО", "ЮВАО",
                                                                        "ЗАО", "СВАО", "ВАО", "ЮЗАО", "СЗАО", "ЦАО"])
        self.option_menu_district.grid(row=3, column=2, padx=20, pady=(5, 10), sticky="w")
        self.metro_label = customtkinter.CTkLabel(self.frame_4, text="Метро:",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"),
                                                  anchor="w")
        self.metro_label.grid(row=4, column=2, padx=20, pady=(15, 5), sticky="w")
        self.entry_ceiling_metro = customtkinter.CTkEntry(self.frame_4, width=200, placeholder_text=" с заглавной буквы")
        self.entry_ceiling_metro.grid(row=5, column=2, padx=(20, 10), pady=(10, 20), sticky="w")

        # create fifth frame with widgets
        self.frame_5 = customtkinter.CTkFrame(self)
        # TODO пока rowspan=2, но еслм добавлять кнопку "очистить фильтр", то нужно заменить на rowspan=1 и добавить фрейм
        self.frame_5.grid(row=0, column=3, rowspan=2, sticky="nsew")
        self.house_type_label = customtkinter.CTkLabel(self.frame_5, text="Тип дома:",
                                                       font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.house_type_label.grid(row=1, column=3, padx=20, pady=(20, 5), sticky="w")
        self.option_menu_house_type = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                                  values=["кирпичный", "блочный", "монолитно-кирпичный",
                                                                          "панельный", "монолитный",
                                                                          "панельный, монолитный",
                                                                          "панельный, кирпичный", "пропущено"])
        self.option_menu_house_type.grid(row=2, column=3, padx=20, pady=(5, 15))
        self.option_menu_house_type.set("пропущено")
        self.parking_label = customtkinter.CTkLabel(self.frame_5, text="Парковка:",
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.parking_label.grid(row=3, column=3, padx=20, pady=(20, 10), sticky="w")
        self.option_menu_parking = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                               values=["стихийная", "наземная", "подземная",
                                                                       "гостевая", "открытая",
                                                                       "многоуровневая", "на крыше",
                                                                       "отдельная многоуровневая",
                                                                       "подземная, гостевая",
                                                                       "подземная, отдельная многоуровневая",
                                                                       "отдельная многоуровневая, гостевая",
                                                                       "подземная, отдельная многоуровневая, гостевая"])
        self.option_menu_parking.grid(row=4, column=3, padx=20, pady=(5, 20))
        self.option_menu_parking.set("стихийная")
        self.heating_label = customtkinter.CTkLabel(self.frame_5, text="Отопление:",
                                                    font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.heating_label.grid(row=5, column=3, padx=20, pady=(15, 5), sticky="w")
        self.option_menu_heating = customtkinter.CTkOptionMenu(self.frame_5, dynamic_resizing=False, width=200,
                                                               values=["центральное", "котел/квартирное отопление",
                                                                       "индивидуальный тепловой пункт",
                                                                       "автономная котельная"])
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

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Стоимость квартиры")
        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="РАССЧИТАТЬ", fg_color="transparent",
                                                     border_width=2,
                                                     font=customtkinter.CTkFont(size=14, weight="bold"),
                                                     text_color=("gray10", "#DCE4EE"), command=self.calculate_price)
        self.main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create main button

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def calculate_price(self):
        ...


# TODO нужно обновлять состояние main entry, чтобы туда ничего нельзя было записать
#  уже в функции calculate_price
#  text.configure(state='normal')
# text.insert('end', 'Some Text')
# text.configure(state='disabled')


app = GUIApp()
app.mainloop()
