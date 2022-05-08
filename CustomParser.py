import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from datetime import date

class CustomsParser():
    def __init__(self):
        self.url = "https://customs.gov.ru"
        self.header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Cookie": "_ym_uid=1645202481635750808; _ym_d=1645202481; sayt_fts_rossii_session=eyJpdiI6IkVUY3YzZzNQYk94RklLYmgrSWM2bmc9PSIsInZhbHVlIjoiSEk3ZlU3OEVWRmwrT01wS3lUbG9SXC9kMnRDbGxoU0pxQXIxVnVTOWZvMjllaGhZOVhtVlRjZ1Uzb1ArNTI5cXlEbjVCYVpMQTJ1OHR6MitFU3FvRWxhWkIyZ3VsbzJBTDZwQXhpQ3ZiMmJWcDIzNG1sR1FrRDJaVGNhUGNPS3NOIiwibWFjIjoiMzM4ZTEwYzM3YThhNTViZGZiNTI2MWMyMTY1NDNlODVlMzZhMzcyOTEyNTM2OGQyMTkyNmE5NzZjZDdkOGE5MiJ9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Site": 'none'}
        #self.initial_soup = self.get_soup(self.url)
        #self.dict_of_countries = self.get_list_of_countries()

    def get_soup(self, url):
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        return soup

    def get_regions_overal(self):
        url = "https://customs.gov.ru/folder/527"
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        regions_overal = soup.find(id="document-325963").a.get("href")
        url = self.url + regions_overal
        responce = requests.get(url, headers=self.header)
        output = open('RegionsOveral.xlsx', 'wb')
        output.write(responce.content)
        output.close()
        df = self.get_regions_from_excel()
        return df

    def get_regions_from_excel(self):
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




