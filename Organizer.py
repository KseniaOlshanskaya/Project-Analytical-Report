import pandas as pd
from RussianTradeParser import RussianTradeParser
from FigureMaker import FigureMaker
from CustomParser import CustomsParser
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from Interface import Interface
from TableMaker import TableMaker


class Organizer:

    def get_report(self):
        #parser1 = RussianTradeParser()
        parser2 = CustomsParser()
        #interface = Interface(parser1, parser2)
        country = "Бангладеш"
        year_previous = 2020
        year_current = 2021
        region = "Новосибирская область"
        '''
        soup = parser1.get_soup_by_country(country) #Возвращает соуп страничку репорта (экспорт + импорт)
        # Общая информация по ВЭД России и страны
        overal_info = parser1.get_overal_information(soup)
        # Все таблицы (экспорт + импорт)
        all_tables = parser1.get_tables(soup)
        # Таблица по экспорту
        pd.set_option('display.max_columns', None)
        df_export_country = parser1.get_product_data_frame(all_tables[0])
        df_import_country = parser1.get_product_data_frame(all_tables[1], export=False)

        # Таблица 1. Основные показатели Россия - страна
        summ_export_russia_previous = sum(df_export_country["ExportPreviousYear"].to_list())/1000
        summ_import_russia_previous = sum(df_import_country["ImportPreviousYear"].to_list())/1000
        summ_export_russia_current = sum(df_export_country["ExportCurrentYear"].to_list())/1000
        summ_import_russia_current = sum(df_import_country["ImportCurrentYear"].to_list())/1000
        table_overal_russia = TableMaker.get_table_overal(summ_export_russia_previous, summ_export_russia_current,
                                                          summ_import_russia_previous, summ_import_russia_current,
                                                          year_previous, year_current)

        # Таблица 2. Структура экспорта, импорта Россия - страна
        products_export_current = self.get_grouped_current(df_export_country)
        products_import_current = self.get_grouped_current(df_import_country, export=False)
        table_structure_russia = TableMaker.get_table_structure(products_export_current, products_import_current)

        # График 1 (пайчарт). экспорт + импорт
        export_values_current, export_labels_current = \
            self.get_data_grouped_by_sector(products_export_current)

        import_values_current, import_labels_current = \
            self.get_data_grouped_by_sector(products_import_current)
        description = "Структура экспорта России по отраслям за " \
                      + str(year_current) + " с страной: " + country
        file_name = 'ExportRussiaPie.png'
        FigureMaker().make_pie_chart(export_values_current, export_labels_current, description, file_name)
        description = "Структура импорта России по отраслям за " \
                      + str(year_current) + " с страной: " + country
        file_name = 'ImportRussiaPie.png'
        FigureMaker().make_pie_chart(import_values_current, import_labels_current, description, file_name)

        # График 2 (Барчарт).
        # Экспорт
        products_export_previous = self.get_grouped_previous(df_export_country)
        products_export_current = self.get_grouped_current(df_export_country)
        export_previous, export_current = \
            self.check_part(products_export_previous, products_export_current)
        labels = self.get_shot_labels(export_current.keys())
        table_for_barchart = TableMaker.get_table_for_bar_chart(export_previous.values(), export_current.values(),
                                                                labels, year_previous, year_current)

        description = 'Динамика экспорта России в страну: ' + country + ' по основным товарным группам'
        file_name = 'ExportRussiaBar.png'
        FigureMaker.make_double_bar_chart(table_for_barchart, description, file_name)

        # График 2 (Барчарт).
        # Импорт
        products_import_previous = self.get_grouped_previous(df_import_country, export=False)
        products_import_current = self.get_grouped_current(df_import_country, export=False)
        import_previous, import_current = \
            self.check_part(products_import_previous, products_import_current)
        labels = self.get_shot_labels(import_current.keys())
        table_for_barchart = TableMaker.get_table_for_bar_chart(import_previous.values(), import_current.values(),
                                                                labels, year_previous, year_current)
        description = 'Динамика импорта России в страну: ' + country + ' по основным товарным группам'
        file_name = 'ImportRussiaBar.png'
        # Barchart for import
        FigureMaker.make_double_bar_chart(table_for_barchart, description, file_name)
        '''
        # Регион - страна
        # Таблица 1. Основные показатели Россия - страна

        docs_links = parser2.get_docs_links(region, year_current, country)
        '''
        name = "RegionFrom_4.xlsx"
        form = 4
        parser2.get_doc_by_form(docs_links, name, form) # Скачивает документ
        df_form4 = parser2.get_df_doc4(name, year_current)
        export_previous = df_form4[str(year_previous)].to_list()[1]
        export_current = df_form4[str(year_current)].to_list()[1]
        import_previous = df_form4[str(year_previous)].to_list()[2]
        import_current = df_form4[str(year_current)].to_list()[2]
        table_overal_region = TableMaker.get_table_overal(export_previous, export_current,
                                                          import_previous, import_current,
                                                          year_previous, year_current)'''

        name = "RegionFrom_6.xlsx"
        form = 6
        #parser2.get_doc_by_form(docs_links, name, form)  #Скачивается документ
        df_form6 = parser2.get_df_doc6(name)
        TableMaker.get_table_structure_region(df_form6, country)
        '''
        df_country6 = df_form6[df_form6["Страна/Товар" ] == country.upper()]
        df_form6 = df_form6.drop(labels=[0, 1, 2], axis=0)
        groups = []
        for row in df_form6.itertuples():
            group = self.get_group(int(row[1]))
            groups.append(group)
        df_form6["Group"] = groups
        export_current = self.get_grouped_current(df_form6)
        import_current = self.get_grouped_current(df_form6, export=False)
        values, labels, description = self.get_data_grouped_by_sector(export_current)
        description = "Структура экспорта НСО по отраслям за 2021 год. с страной: " + country
        FigureMaker().make_pie_chart(values, labels, description)

        values, labels, description = self.get_data_grouped_by_sector(import_current)
        description = "Структура импорта НСО по отраслям за 2021 год. с страной: " + country
        FigureMaker().make_pie_chart(values, labels, description, export=False)'''

        '''
        # ВСЕГО (одна строчка) по региону (экспорт + импорт)
        name = "RegionFrom_8.xlsx"
        form = 8
        parser2.get_doc_by_form(docs_links, name, form)
        df_form8 = parser2.get_df_doc8(name)
        
        context = {}
        doc = DocxTemplate("Template.docx")
        with open("Kazakhstan.txt", "r", encoding="UTF-8") as file:
            text = file.readline()
        context['country'] = country
        context['region'] = 'Новосибирская область'
        context['year'] = '2021'
        context['Текст'] = text
        imagen = InlineImage(doc, 'ExportRussiaPie.png', width=Mm(150))  # width is in millimetres
        context['image'] = imagen
        doc.render(context)
        # сохраняем и смотрим, что получилось
        doc.save("generated_docu.docx")'''

    @staticmethod
    def get_grouped_current(df, export=True):
        if export:
            products = df.groupby('Group')["ExportCurrentYear"].sum().to_dict()
            print(products)
        else:
            products = df.groupby('Group')["ImportCurrentYear"].sum().to_dict()
            print(products)
        return products

    @staticmethod
    def check_part(products_export_previous, products_export_current):
        products_export_previous_new = {}
        products_export_current_new = {}
        summ_previous = sum(products_export_previous.values())
        summ_current = sum(products_export_current.values())
        for product_group in products_export_previous.keys():
            part_previous = products_export_previous[product_group] / summ_previous
            part_current = products_export_current[product_group] / summ_current
            if part_previous < 0.03 or part_current < 0.03:
                pass
            else:
                products_export_previous_new[product_group] = products_export_previous[product_group]
                products_export_current_new[product_group] = products_export_current[product_group]
        return products_export_previous_new, products_export_current_new

    @staticmethod
    def get_grouped_previous(df, export=True):
        if export:
            products = df.groupby('Group')["ExportPreviousYear"].sum().to_dict()
        else:
            products = df.groupby('Group')["ImportPreviousYear"].sum().to_dict()
        return products

    @staticmethod
    def get_data_grouped_by_sector(products):
        all_values_summ = sum(products.values())
        keys = [key for key in products if
                products.get(key) / all_values_summ < 0.03 and key != "Прочие товары"]
        extra = [products.get(key) for key in keys]
        summ_extra = sum(extra) + products["Прочие товары"]
        for key in keys:
            products.pop(key)
        products.update({"Прочие товары": summ_extra})
        values = products.values()
        labels = products.keys()
        return values, labels

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
            if label == "Продовольственные товары и сырье":
                shot_labels.append("Продовольствие")
            if label == "Минеральные продукты":
                shot_labels.append("Минералы")
            if label == "Топливно-энергетические товары":
                shot_labels.append("Топливо")
            if label == "Продукция химической промышленности":
                shot_labels.append("Химия")
            if label == "Кожевенное сырье, пушнина и изделия":
                shot_labels.append("Кожа")
            if label == "Древесина, целлюлозно-бумажные изделия":
                shot_labels.append("Древесина")
            if label == "Металлы и изделия из них":
                shot_labels.append("Металлы")
            if label == "Текстиль, текстильные изделия и обувь":
                shot_labels.append("Текстиль")
            if label == "Машиностроительная продукция":
                shot_labels.append("Машины")
            if label == "Прочие товары":
                shot_labels.append("Прочие товары")
        return shot_labels

    def get_group(self, id):
        if id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]:
            return "Продовольственные товары и сырье"
        if id in [25, 26]:
            return "Минеральные продукты"
        if id in [27]:
            return "Топливно-энергетические товары"
        if id in [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:
            return "Продукция химической промышленности"
        if id in [41, 42, 43]:
            return "Кожевенное сырье, пушнина и изделия"
        if id in [44, 45, 46, 47, 48, 49]:
            return "Древесина, целлюлозно-бумажные изделия"
        if id in [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]:
            return "Металлы и изделия из них"
        if id in [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]:
            return "Текстиль, текстильные изделия и обувь"
        if id in [84, 85, 86, 87, 88, 89, 90]:
            return "Машиностроительная продукция"
        else:
            return "Прочее"






