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

        products_export_current = self.get_grouped_current(df_export)
        values_current, labels_current, description_current = \
            self.get_data_grouped_by_sector(products_export_current) # Export Data for piechart (2021)

        # Piechart for export
        FigureMaker().make_pie_chart(values_current, labels_current, description_current)

        # Barchart for export
        products_export_previous = self.get_grouped_previous(df_export)
        products_export_current = self.get_grouped_current(df_export)
        values_current = products_export_current.values()
        labels_current = products_export_current.keys()
        values_previous = products_export_previous.values()
        values_prev = [val / 1000000 for val in values_previous]
        values_cur = [val / 1000000 for val in values_current]
        labels = self.get_shot_labels(labels_current)
        FigureMaker.make_double_bar_chart(values_prev, values_cur, labels)

        # Таблица по импорту
        df_import = self.parser.get_product_data_frame(all_tables[1], export=False)
        products_import_current = self.get_grouped_current(df_import, export=False)
        values, labels, description =self.get_data_grouped_by_sector(products_import_current, export=False) # Import Data for piechart (2021)

        # Piechart for import
        FigureMaker().make_pie_chart(values, labels, description, export=False)

        products_import_previous = self.get_grouped_previous(df_import, export=False)
        products_import_current = self.get_grouped_current(df_import, export=False)
        values_current = products_import_current.values()
        values_cur = [val / 1000000 for val in values_current]
        labels_current = products_import_current.keys()
        values_previous = products_import_previous.values()
        values_prev = [val / 1000000 for val in values_previous]
        labels = self.get_shot_labels(labels_current)
        # Barchart for import
        FigureMaker.make_double_bar_chart(values_prev, values_cur, labels, export=False)


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
    def get_data_grouped_by_sector(products, export=True):
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

    @staticmethod
    def get_shot_labels(labels):
        shot_labels = []
        for label in labels:
            if label == "Продовольственные товары":
                shot_labels.append("Продовольствие")
            if label == "Сельхозтовары":
                shot_labels.append("Сельхозтовары")
            if label == "Машины, оборудование и ТС":
                shot_labels.append("Машины")
            if label == "Древесина и целлюлозно-бумажные изделия":
                shot_labels.append("Древесина")
            if label == "Продукция химической промышленности":
                shot_labels.append("Химия")
            if label == "Топливно-энергетические товары":
                shot_labels.append("Энергоносители")
            if label == "Металлы и изделия из них":
                shot_labels.append("Металлы")
            if label == "Кожевенное сырье, пушнина и изделия из них":
                shot_labels.append("Кожа")
            if label == "Текстиль, текстильные изделия и обувь":
                shot_labels.append("Текстиль")
            if label == "Драгоценные камни, драгоценные металлы и изделия из них":
                shot_labels.append("Драг.камни")
            if label == "Прочее":
                shot_labels.append("Прочее")
        return shot_labels






