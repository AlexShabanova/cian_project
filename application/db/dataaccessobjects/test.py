def get_flat_general_info_names_values(self) -> Dict[str, str]:
    """Получение заголовков и значений блока информации о доме"""
    names_values_dict = dict()
    try:
        flat_information = self.soup.find_all('li', class_='a10a3f92e9--item--d9uzC')
        for el in flat_information:
            try:
                name = el.find('span',
                               class_='a10a3f92e9--name--x7_lt').text
                value = el.find('span',
                                class_='a10a3f92e9--value--Y34zN').text
                names_values_dict[name] = value
            except Exception as err:
                pass
    except Exception as err:
        pass



    def get_flat_general_info(self, flat_general_info_names_values: Dict[str, str]) -> List[Union[str, float]]:
        """Получение общей информации о квартире (Тип жилья, Планировка, Высота потолков,
         Санузел, Балкон/лоджия, Ремонт, Вид из окон, Отделка)"""
        built_year, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition = None, None, None, None, None, None, None, None, None

        for name, value in names_values_dict.items():
            if name == 'Год постройки':
                built_year = int(value)
            if name == 'Тип жилья':
                if 'Вторичка' in value:
                    housing_type = 'вторичное'
                elif 'Новостройка' in value:
                    housing_type = 'новостройка'
            elif name == 'Планировка':
                if 'Изолированная' in value:
                    planning = 'изолированная'
                elif 'Смежная' in value:
                    planning = 'смежная'
                elif 'Смежно-изолированная' in value:
                    planning = 'смежно-изолированная'
            elif name == 'Высота потолков':
                ceiling_height = atof(value.text.split(' ')[0])
            elif name == 'Санузел':
                bathroom = value
            elif name == 'Балкон/лоджия':
                balcony_loggia = value
            elif name == 'Ремонт':
                if 'Без ремонта' in value:
                    repair = 'без ремонта'
                elif 'Евроремонт' in value:
                    repair = 'евроремонт'
                elif 'Косметический' in value:
                    repair = 'косметический'
                elif 'Дизайнерский' in value:
                    repair = 'дизайнерский'
            elif name == 'Вид из окон':
                if 'Во двор' in value:
                    view = 'во двор'
                elif 'На улицу' in value:
                    view = 'на улицу'
                elif 'На улицу и двор' in value:
                    view = 'на улицу и двор'
            elif name == 'Отделка':
                if 'Черновая' in value:
                    view = 'черновая'
                elif 'Чистовая' in value:
                    view = 'чистовая'
                elif 'Предчистовая' in value:
                    view = 'предчистовая'
                elif 'Нет' in value:
                    view = 'нет'
        return [built_year, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                finished_shell_condition]


#  старый код с двумя функциями для получения имен заголовков и значений
    def get_flat_general_info_names(self) -> List[Tag]:
        """Получение заголовков блока общей информации о квартире (тип жилья, высота потолков, санузел и пр.)"""
        try:
            return self.soup.find('ul', {'class': 'a10a3f92e9--list--jHl8z'}).find_all('span', {
                'class': 'a10a3f92e9--name--x7_lt'})
        except Exception as err:
            return []

    def get_flat_general_info_values(self) -> List[Tag]:
        """Получение значений для заголовков блока общей информации о квартире (тип жилья, высота потолков, санузел и пр.)"""
        try:
            return self.soup.find('ul', {'class': 'a10a3f92e9--list--jHl8z'}).find_all('span', {
                'class': 'a10a3f92e9--value--Y34zN'})
        except Exception as err:
            return []

    def get_flat_general_info(self, flat_general_info_names: List[Tag],
                              flat_general_info_values: List[Tag]) -> List[Union[str, float]]:
        """Получение общей информации о квартире (Тип жилья, Планировка, Высота потолков,
         Санузел, Балкон/лоджия, Ремонт, Вид из окон, Отделка)"""
        built_year, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view, finished_shell_condition = None, None, None, None, None, None, None, None, None

        for name_value in zip(flat_general_info_names, flat_general_info_values):
            if name_value[0].text == 'Год постройки':
                built_year = int(name_value[1].text)
            if name_value[0].text == 'Тип жилья':
                if 'Вторичка' in name_value[1].text:
                    housing_type = 'вторичное'
                elif 'Новостройка' in name_value[1].text:
                    housing_type = 'новостройка'
            elif name_value[0].text == 'Планировка':
                if 'Изолированная' in name_value[1].text:
                    planning = 'изолированная'
                elif 'Смежная' in name_value[1].text:
                    planning = 'смежная'
                elif 'Смежно-изолированная' in name_value[1].text:
                    planning = 'смежно-изолированная'
            elif name_value[0].text == 'Высота потолков':
                ceiling_height = atof(name_value[1].text.split(' ')[0])
            elif name_value[0].text == 'Санузел':
                bathroom = name_value[1].text
            elif name_value[0].text == 'Балкон/лоджия':
                balcony_loggia = name_value[1].text
            elif name_value[0].text == 'Ремонт':
                if 'Без ремонта' in name_value[1].text:
                    repair = 'без ремонта'
                elif 'Евроремонт' in name_value[1].text:
                    repair = 'евроремонт'
                elif 'Косметический' in name_value[1].text:
                    repair = 'косметический'
                elif 'Дизайнерский' in name_value[1].text:
                    repair = 'дизайнерский'
            elif name_value[0].text == 'Вид из окон':
                if 'Во двор' in name_value[1].text:
                    view = 'во двор'
                elif 'На улицу' in name_value[1].text:
                    view = 'на улицу'
                elif 'На улицу и двор' in name_value[1].text:
                    view = 'на улицу и двор'
            elif name_value[0].text == 'Отделка':
                if 'Черновая' in name_value[1].text:
                    view = 'черновая'
                elif 'Чистовая' in name_value[1].text:
                    view = 'чистовая'
                elif 'Предчистовая' in name_value[1].text:
                    view = 'предчистовая'
                elif 'Нет' in name_value[1].text:
                    view = 'нет'
        return [built_year, housing_type, planning, ceiling_height, bathroom, balcony_loggia, repair, view,
                finished_shell_condition]