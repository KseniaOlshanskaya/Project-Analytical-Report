from RussianTradeParser import RussianTradeParser
import matplotlib.pyplot as plt
from FigureMaker import FigureMaker
from fpdf import FPDF
from PDFCreator import PDF

class Organizator():
    def __init__(self):
        self.parser = RussianTradeParser()

    def get_report(self):
        soup = self.parser.get_soup_by_country("Казахстан") #Возвращает соуп страничку репорта (экспорт + импорт)

        # Нам нужна общая информация
        overal_info = self.parser.get_overal_information(soup)

        # Достаю все таблицы (экспорт + импорт)
        all_tables = self.parser.get_tables(soup)

        # Таблица по экспорту
        df_export = self.parser.get_product_data_frame(all_tables[0])
        products = self.get_grouped_current(df_export)
        values, labels, description = self.get_data_for_piechart(products) # Export Data for piechart (2021)

        # Piechart for export
        FigureMaker().makePieChart(values, labels, description)

        # Barchart for export


        # Таблица по импорту
        df_import = self.parser.get_product_data_frame(all_tables[1], export=False)
        products = self.get_grouped_current(df_import, export=False)
        values, labels, description =self.get_data_for_piechart(products) # Import Data for piechart (2021)

        # Piechart for import
        FigureMaker().makePieChart(values, labels, description, export=False)



    @staticmethod
    def get_grouped_current(df, export=True):
        if export:
            products = df.groupby('Group')["ExportCurrentYear"].sum().to_dict()
        else:
            products = df.groupby('Group')["ImportCurrentYear"].sum().to_dict()
        return products

    @staticmethod
    def get_grouped_previous(df, export=True):
        if export:
            products = df.groupby('Group')["ExportPreviousYear"].sum().to_dict()
        else:
            products = df.groupby('Group')["ImportPreviousYear"].sum().to_dict()
        return products

    @staticmethod
    def get_data_for_piechart(products):
        all_values_summ = sum(products.values())
        keys = [key for key in products if
                products.get(key) / all_values_summ < 0.03 and key != "Прочее"]
        extra = [products.get(key) for key in keys]
        summ_extra = sum(extra) + products["Прочее"]
        for key in keys:
            products.pop(key)
        products.update({"Прочее": summ_extra})
        values = products.values()
        labels = products.keys()
        if export:
            description = "Структура экспорта России по отраслям за 2021 год. с страной: " + "Казахстан"
        else:
            description = "Структура импорта России по отраслям за 2021 год. с страной: " + "Казахстан"
        return values, labels, description




WIDTH = 210



