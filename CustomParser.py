import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from datetime import date

class CustomsParser():
    def __init__(self):
        self.header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Cookie": "_ym_uid=1645202481635750808; _ym_d=1645202481; sayt_fts_rossii_session=eyJpdiI6IkVUY3YzZzNQYk94RklLYmgrSWM2bmc9PSIsInZhbHVlIjoiSEk3ZlU3OEVWRmwrT01wS3lUbG9SXC9kMnRDbGxoU0pxQXIxVnVTOWZvMjllaGhZOVhtVlRjZ1Uzb1ArNTI5cXlEbjVCYVpMQTJ1OHR6MitFU3FvRWxhWkIyZ3VsbzJBTDZwQXhpQ3ZiMmJWcDIzNG1sR1FrRDJaVGNhUGNPS3NOIiwibWFjIjoiMzM4ZTEwYzM3YThhNTViZGZiNTI2MWMyMTY1NDNlODVlMzZhMzcyOTEyNTM2OGQyMTkyNmE5NzZjZDdkOGE5MiJ9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Site": 'none'}
        self.region_links = self.get_region_links()
        #self.sib = self.get_siberian_district_soup()
        #self.reg = self.get_region_soup(region)
        #self.district_docs = self.get_docs(self.sib)
        #self.region_docs = []
        #self.district_url = "https://stu.customs.gov.ru"
        #self.initial_soup = self.get_soup(self.url)
        #self.dict_of_countries = self.get_list_of_countries()

    def get_docs_links(self, region, year, country):
        year_link =""
        region_link = self.region_links[region]
        soup = self.get_soup(region_link)
        divs = soup.find_all("div", class_="section-link__item")
        for div in divs:
            year_item = div.find("div", class_="section-link__item--text "
                                                 "col-12 col-sm-12 pr-0 pl-0").text.strip()[:4]
            if year == int(year_item):
                year_link = div.a.get("href")
                break
        soup = self.get_soup(year_link)
        report_links = soup.find("div", class_="pin").find_all("a")
        report_link = ""
        indicator = "за "+ str(year) +" год"
        for link in report_links:
            if indicator in link.text:
                report_link = link.get("href")
        soup = self.get_soup(report_link)
        doc_links = self.get_docs(soup)
        return doc_links

    def get_doc_by_form(self, docs_links, name, form):
        url = ""
        form = str(form)
        for doc in docs_links:
            if form in doc:
                url = doc
                break
        responce = requests.get(url, headers=self.header)
        output = open(name, 'wb')
        output.write(responce.content)
        output.close()

    def get_df_doc4(self, name, year):
        df = pd.read_excel(name)
        year_previous = str(year - 1)
        year_current = str(year)
        df = df.dropna()
        pd.set_option('display.max_columns', None)
        df = df.drop(labels=["Unnamed: 1", "Unnamed: 3", "Unnamed: 5"], axis=1)
        df = df.rename(columns={df.columns[0]: 'Показатель',
                                df.columns[1]: year_previous,
                                df.columns[2]: year_current,
                                df.columns[3]: "Темп роста"
                                })
        return df

    def get_df_doc6(self, name):
        df = pd.read_excel(name)
        df = df.dropna()
        df = df.rename(columns={df.columns[0]: 'Код ВЭД',
                                df.columns[1]: 'Страна/Товар',
                                df.columns[2]: 'Экспорт',
                                df.columns[3]: 'Импорт'
                                })
        return df

    def get_df_doc8(self, name):
        df = pd.read_excel(name)
        df = df.dropna()
        pd.set_option('display.max_columns', None)
        df = df.drop(labels=["Unnamed: 2", "Unnamed: 4", "Unnamed: 6", "Unnamed: 7",
                             "Unnamed: 8", "Unnamed: 9",
                             "Unnamed: 10", "Unnamed: 11",
                             "Unnamed: 12", "Unnamed: 13"], axis=1)
        df = df.rename(columns={df.columns[0]: 'Товарная группа',
                                df.columns[1]: 'Наименование',
                                df.columns[2]: 'Экспорт',
                                df.columns[3]: 'Импорт'
                                })
        return df

    def get_soup(self, url):
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        return soup

    def get_siberian_district_soup(self):
        url = "https://stu.customs.gov.ru/document/text/330148"
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        return soup

        responce = requests.get(url, headers=self.header)
        output = open('RegionsOveral.xlsx', 'wb')
        output.write(responce.content)
        output.close()
        df = self.get_regions_overal_from_excel()
        return df

    def get_region_links(self):
        url = "https://stu.customs.gov.ru/folder/143386"
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        divs = soup.find_all("div", class_="section-link__item")
        dict_links = {}
        for div in divs:
            region_name = div.find("div", class_="section-link__item--text "
                              "col-12 col-sm-12 pr-0 pl-0").text.strip()
            href = div.a.get("href")
            dict_links.update({region_name: href})
        return dict_links


    def get_docs(self, soup):
        divs = soup.find_all("div", class_="doc__desc")
        doc_links = ["https://stu.customs.gov.ru" + i.a.get("href") for i in divs]
        return doc_links

    def get_regions_overal_from_excel(self):
        df = pd.read_excel("RegionsOveral.xlsx", sheet_name="Внешняя торговля субъектов РФ в")
        pd.set_option('display.max_columns', None)
        df.rename(columns={'Unnamed: 1': 'ЭкспортДальнееЗарубежье',
                           'Unnamed: 2': 'ЭкспортСНГ',
                           'Unnamed: 3': 'ЭкспортВсего',
                           'Unnamed: 4': 'ЭкспортДоляОтОбщего',
                           'Unnamed: 5': 'ИмпортДальнееЗарубежье',
                           'Unnamed: 6': 'ИмпортСНГ',
                           'Unnamed: 7': 'ИмпортВсего',
                           'Unnamed: 8': 'ИмпортДоляОтОбщего',
                           'Unnamed: 9': 'Сальдо'},
                  inplace=True)
        df = df.drop(labels=[0, 1, 2], axis=0)
        return df




