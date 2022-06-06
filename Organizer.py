import pandas as pd
from RussianTradeParser import RussianTradeParser
from FigureMaker import FigureMaker
from CustomParser import CustomsParser
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from Interface import Interface


class Organizer:

    def get_report(self):
        parser1 = RussianTradeParser()
        parser2 = CustomsParser()
        interface = Interface(parser1, parser2)

        soup = parser1.get_soup_by_country("Казахстан") #Возвращает соуп страничку репорта (экспорт + импорт)

        # Нам нужна общая информация
        overal_info = parser1.get_overal_information(soup)

        # Достаю все таблицы (экспорт + импорт)
        all_tables = parser1.get_tables(soup)

        # Таблица по экспорту
        pd.set_option('display.max_columns', None)
        df_export = parser1.get_product_data_frame(all_tables[0])
        print(df_export)
        df_import = parser1.get_product_data_frame(all_tables[1], export=False)

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

        print(df_summary_russia)
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
        values_prev.pop(2)
        values_cur.pop(2)
        labels.pop(2)
        values_prev.pop(7)
        values_cur.pop(7)
        labels.pop(7)
        values_prev.pop(0)
        values_cur.pop(0)
        labels.pop(0)
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
        values_prev.pop(0)
        values_cur.pop(0)
        labels.pop(0)
        values_prev.pop(0)
        values_cur.pop(0)
        labels.pop(0)
        values_prev.pop(0)
        values_cur.pop(0)
        labels.pop(0)
        values_prev.pop(4)
        values_cur.pop(4)
        labels.pop(4)
        values_prev.pop(4)
        values_cur.pop(4)
        labels.pop(4)
        # Barchart for import
        FigureMaker.make_double_bar_chart(values_prev, values_cur, labels, export=False)



        docs_links = parser2.get_docs_links("Новосибирская область", 2021, "Казахстан")

        name = "RegionFrom_4.xlsx"
        form = 4
        parser2.get_doc_by_form(docs_links, name, form)
        form4 = parser2.get_df_doc4(name, 2021)

        name = "RegionForm6.xlsx"
        form = 6
        #customs.get_doc_by_form(docs_links, name, form)
        df_form6 = parser2.get_df_doc6(name)

        df_all = df_form6[df_form6["Страна/Товар" ]== "ВСЕГО"]
        df_country6 = df_form6[df_form6["Страна/Товар" ]== "КАЗАХСТАН"]
        df_form6 = df_form6.drop(labels=[0, 1, 2], axis=0)
        groups = []
        for row in df_form6.itertuples():
            group = self.get_group(int(row[1]))
            groups.append(group)
        df_form6["Group"] = groups
        export_current = self.get_grouped_current(df_form6)
        import_current = self.get_grouped_current(df_form6, export=False)
        values, labels, description = self.get_data_grouped_by_sector(export_current)
        description = "Структура экспорта НСО по отраслям за 2021 год. с страной: " + "Казахстан"
        FigureMaker().make_pie_chart(values, labels, description)

        values, labels, description = self.get_data_grouped_by_sector(import_current)
        description = "Структура импорта НСО по отраслям за 2021 год. с страной: " + "Казахстан"
        FigureMaker().make_pie_chart(values, labels, description, export=False)


        name = "RegionFrom_8.xlsx"
        form = 8
        parser2.get_doc_by_form(docs_links, name, form)
        form8 = parser2.get_df_doc8(name)

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
        doc.save("generated_docu.docx")


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

    def get_group(self, id):
        if id in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]:
            return "Продовольственные товары"
        if id in [6, 12, 13, 14, 31]:
            return "Сельхозтовары"
        if id in [84, 85, 86, 87, 88, 89, 90]:
            return "Машины, оборудование и ТС"
        if id in [44, 45, 46, 47, 48, 49, 94]:
            return "Древесина и целлюлозно-бумажные изделия"
        if id in [28, 29, 30, 32, 33, 34, 35, 36, 38, 39, 40]:
            return "Продукция химической промышленности"
        if id in [25, 26, 27]:
            return "Топливно-энергетические товары"
        if id in [72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83]:
            return "Металлы и изделия из них"
        if id in [41, 42, 43]:
            return "Кожевенное сырье, пушнина и изделия из них"
        if id in [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]:
            return "Текстиль, текстильные изделия и обувь"
        if id == 71:
            return "Драгоценные камни, драгоценные металлы и изделия из них"
        else:
            return "Прочее"






