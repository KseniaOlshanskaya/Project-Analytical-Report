import pandas as pd
from RussianTradeParser import RussianTradeParser

class TableMaker:

    @staticmethod
    def get_table_overal(export_previous, export_current,
                    import_previous, import_current,
                    year_previous,year_current):
        df = pd.DataFrame({"Показатель": [str(year_previous) ,str(year_current)],
                           "Экспорт, тыс. дол": [export_previous, export_current],
                           "Импорт, тыс. дол": [import_previous, import_current],
                           "Внешнеторговый оборот, тыс. дол": [export_previous + import_previous, export_current + import_current],
                           "Сальдо, тыс. дол": [export_previous - import_previous, export_current - import_current]})
        return df

    @staticmethod
    def get_table_structure(dict_export, dict_import):
        product_names = ["Продовольственные товары и сырье", "Минеральные продукты", "Топливно-энергетические товары",
                         "Продукция химической промышленности", "Кожевенное сырье, пушнина и изделия",
                         "Древесина, целлюлозно-бумажные изделия", "Текстиль, текстильные изделия и обувь", "Металлы и изделия из них",
                         "Машиностроительная продукция", "Прочие товары"]
        list_export = []
        list_import = []
        for name in product_names:
            if name in dict_export.keys():
                product_summ_export = dict_export[name]
            else:
                product_summ_export = 0
            list_export.append(product_summ_export)
            if name in dict_import.keys():
                product_summ_import = dict_import[name]
            else:
                product_summ_import = 0
            list_import.append(product_summ_import)

        product_codes = ["1-24", "25-26", "27","28-40", "41-43",
                         "44-49", "50-67","72-83", "84-90",
                         "68-71, 91-98"]
        df = pd.DataFrame({"Код ТН ВЭД": product_codes, "Наименование сегмента товаров": product_names,
                           "Экспорт, тыс. дол": list_export, "Импорт, тыс. дол": list_import})
        return df

    @staticmethod
    def get_growth_rate_table(export_previous, export_current, import_previous, import_current):
        amount_previous = export_previous + import_previous
        amount_current = export_current + import_current
        saldo_previous = export_previous - import_previous
        saldo_current = export_current - import_current
        dict_rate = {"Экспорт":[export_previous, export_current],
                     "Импорт": [import_previous, import_current],
                     "Оборот": [amount_previous, amount_current],
                     "Сальдо": [saldo_previous, saldo_current]}
        df = pd.DataFrame({"Показатель": ["Темп роста, %", "Темп прироста, %"]})
        for indicator in dict_rate.keys():
            rate_of_increase = (dict_rate[indicator][1] / dict_rate[indicator][0])*100 # темп роста
            accession_rate = rate_of_increase - 100 # темп прироста
            df[indicator] = [rate_of_increase, accession_rate]
        df = df.T
        return df

    @staticmethod
    def get_parts_table(export_region, export_district, export_country,
                        import_region, import_district, import_country):
        export_part_in_district = export_region/export_district
        export_part_in_country = export_region / export_country
        import_part_in_district = import_region/import_district
        import_part_in_country = import_region / import_country
        df = pd.DataFrame({"Субъект": ["СФО", "РФ"],
                           "Экспорт": [export_part_in_district, export_part_in_country],
                           "Импорт": [import_part_in_district, import_part_in_country]})
        return df

    @staticmethod
    def get_indicators(list_export_region, summ_export_all, summ_import_region, summ_import_all):
        summ_export_region = sum(list_export_region)
        summ_export_all = str(summ_export_all).strip()
        summ_import_all = str(summ_import_all).strip()
        summ_import_region = str(summ_import_region).strip()
        INN = 0
        for product in list_export_region:
            part = (product/summ_export_region)**2
            INN += part
        T = (summ_export_region + float(summ_import_region))/(float(summ_export_all) + float(summ_import_all)) #Индекс значимости
        if INN > 0.5:
            description = "Высокая концентрация экспорта"
        else:
            description = "Низкая концентрация экспорта"

        text = "Доля внешнеторгового оборота со страной"
        df = pd.DataFrame({"Показатель": ["Индекс концентрации экспорта","Индекс взаимной торговли"],
                           "Значение": [INN, T],
                           "Пояснение": [description, text]})
        return df

    @staticmethod
    def get_table_for_bar_chart(values_previous, values_current, labels_previous,
                                year_previous, year_current):

        df = pd.DataFrame({year_previous: values_previous,
                           year_current: values_current},
                           index=labels_previous)
        return df

    @staticmethod
    def get_dict_most_frequent(products_dict):
        dict_most_frequent = {}
        summ_all = sum(products_dict.values())
        for key in products_dict.keys():
            part = products_dict[key] / summ_all
            dict_most_frequent.update({key: part})
        return dict_most_frequent

    @staticmethod
    def get_table_rates_by_sectors(dict_prev, dict_cur):
        df = pd.DataFrame({"Товарная группа": ["Темп роста, %", "Темп прироста, %"]})
        for group in dict_prev:
            if group not in dict_prev.keys() or group not in dict_cur.keys():
                pass
            else:
                rate_of_increase = (dict_cur[group] / dict_prev[group]) * 100  # темп роста
                accession_rate = rate_of_increase - 100  # темп прироста
                df[group] = [rate_of_increase, accession_rate]
        return df

    @staticmethod
    def get_table_structure_region(df, country):
        country_row = df[df['Страны/товары'] == country.upper()].index.to_list()
        df_country_row = df.loc[country_row[0]:country_row[0]+180, ['Страны/товары','Экспорт', 'Импорт']]
        df_country_all = df_country_row[df_country_row['Страны/товары'] == country.upper()]
        df_country_row = df_country_row.drop(df_country_all.index, axis=0)
        df_export = pd.DataFrame(columns=['Group', 'Export'])
        df_import = pd.DataFrame(columns=['Group', 'Import'])
        for row in df_country_row.itertuples():
            if row[2] != 0 or row[3] != 0:
                if not row[1][:2].isalpha():
                    group_name = RussianTradeParser.get_group(int(row[1][:2]))
                    df_export = df_export.append({'Group': group_name, 'Export': row[2]}, ignore_index=True)
                    df_import = df_import.append({'Group': group_name, 'Import': row[3]}, ignore_index=True)
                else:
                    break
        return df_export, df_import
