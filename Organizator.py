import pandas as pd

from RussianTradeParser import RussianTradeParser
import matplotlib.pyplot as plt
from FigureMaker import FigureMaker
from CustomParser import CustomsParser
import itertools
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import itertools


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
        pd.set_option('display.max_columns', None)
        df_export = self.parser.get_product_data_frame(all_tables[0])
        df_import = self.parser.get_product_data_frame(all_tables[1], export=False)

        # Формируем первую таблицу с общими показателями для России
        summ_export_russia_current = sum(df_export["ExportCurrentYear"].to_list())/1000
        summ_import_russia_current = sum(df_import["ImportCurrentYear"].to_list())/1000
        oborot_russia_current =  summ_export_russia_current + summ_import_russia_current
        saldo_russia_current = summ_export_russia_current - summ_import_russia_current

        summ_export_russia_previous = sum(df_export["ExportPreviousYear"].to_list()) / 1000
        summ_import_russia_previous = sum(df_import["ImportPreviousYear"].to_list()) / 1000
        oborot_russia_previous = summ_export_russia_current + summ_import_russia_current
        saldo_russia_previous = summ_export_russia_current - summ_import_russia_current
        df_summary_russia = pd.DataFrame({"Показатель": "Экспорт",
                                          "2021 г., тыс.дол.": summ_export_russia_current,
                                          "2020 г., тыс.дол.": summ_export_russia_previous}, index=[0])
        df_summary_russia = df_summary_russia.append({"Показатель": "Импорт",
                                            "2021 г., тыс.дол.": summ_import_russia_current,
                                            "2020 г., тыс.дол.": summ_import_russia_previous}, ignore_index=True)
        df_summary_russia = df_summary_russia.append({"Показатель": "Оборот",
                                                      "2021 г., тыс.дол.": oborot_russia_current,
                                                      "2020 г., тыс.дол.": oborot_russia_previous}, ignore_index=True)


        products_export_current = self.get_grouped_current(df_export)
        values_current, labels_current, description_current = \
            self.get_data_grouped_by_sector(products_export_current)  # Export Data for piechart (2021)

        # Piechart for export
        description = "Структура экспорта России по отраслям за 2021 год. с страной: " + "Казахстан"
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

        products_import_current = self.get_grouped_current(df_import, export=False)
        values, labels, description = self.get_data_grouped_by_sector(products_import_current,
                                                                      export=False)  # Import Data for piechart (2021)
        # Piechart for import
        description = "Структура импорта России по отраслям за 2021 год. с страной: " + "Казахстан"
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

        customs = CustomsParser()
        docs_links = customs.get_docs_links("Новосибирская область", 2021, "Казахстан")

        name = "RegionFrom_4.xlsx"
        form = 4
        customs.get_doc_by_form(docs_links, name, form)
        customs.get_df_doc4(name, 2021)

        name = "RegionForm6.xlsx"
        form = 6
        #customs.get_doc_by_form(docs_links, name, form)
        customs.get_df_doc6(name)

        name = "RegionFrom_8.xlsx"
        form = 8
        customs.get_doc_by_form(docs_links, name, form)
        customs.get_df_doc8(name)

        context = {}
        doc = DocxTemplate("Template.docx")
        with open("Kazakhstan.txt", "r", encoding="UTF-8") as file:
            text = file.readline()
        context['country'] = 'Казахстан'
        context['region'] = 'Новосибирская область'
        context['year'] = '2021'
        context['Текст'] = text
        imagen = InlineImage(doc, 'ExportRussiaPie.png', width=Mm(150))  # width is in millimetres
        context['image'] = imagen
        doc.render(context)
        # сохраняем и смотрим, что получилось
        doc.save("generated_doc.docx")


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
    def define_district(region):
        pass

    @staticmethod
    def get_district_data(district, df_country):
        pass

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








