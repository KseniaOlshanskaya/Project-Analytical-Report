import pandas as pd


class TableMaker:

    @staticmethod
    def get_table_overal(export_previous, export_current,
                    import_previous, import_current,
                    year_previous,year_current):
        df = pd.DataFrame({"Показатель": [year_previous,year_current],
                           "Экспорт, тыс. дол": [export_previous, export_current],
                           "Импорт, тыс. дол": [import_previous, import_current],
                           "Оборот, тыс. дол": [export_previous + import_previous, export_current + import_current],
                           "Сальдо, тыс. дол": [export_previous - import_previous, export_current - import_current]})
        df = df.T
        return df

    @staticmethod
    def get_table_structure(list_export, list_import):
        product_names = ["Продовольственные товары и сырье", "Минеральные продукты", "Топливно-энергетические товары",
                         "Продукция химической промышленности", "Кожевенное сырье, пушнина и изделия",
                         "Древесина, целлюлосно-бумажные изделия", "Текстиль и обувь", "Металлы и изделия из них",
                         "Машиностроительная продукция", "Прочие товары"]
        product_codes = ["1-24", "25-26", "27","28-40", "41-43",
                         "44-49", "50-67","72-83", "84-90",
                         "68-71, 91-98"]
        df = pd.DataFrame({"Код ТН ВЭД": product_codes, "Наименование сегмента товаров": product_names,
                           "Экспорт, тыс. дол": list_export, "Импорт, тыс. дол": list_import})
        return df


