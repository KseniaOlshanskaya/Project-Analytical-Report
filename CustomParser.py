import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from datetime import date

class CustomsParser():
    def __init__(self):
        self.url = "https://customs.gov.ru/"
        self.header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Cookie": "_ym_uid=1645202481635750808; _ym_d=1645202481; sayt_fts_rossii_session=eyJpdiI6IkVUY3YzZzNQYk94RklLYmgrSWM2bmc9PSIsInZhbHVlIjoiSEk3ZlU3OEVWRmwrT01wS3lUbG9SXC9kMnRDbGxoU0pxQXIxVnVTOWZvMjllaGhZOVhtVlRjZ1Uzb1ArNTI5cXlEbjVCYVpMQTJ1OHR6MitFU3FvRWxhWkIyZ3VsbzJBTDZwQXhpQ3ZiMmJWcDIzNG1sR1FrRDJaVGNhUGNPS3NOIiwibWFjIjoiMzM4ZTEwYzM3YThhNTViZGZiNTI2MWMyMTY1NDNlODVlMzZhMzcyOTEyNTM2OGQyMTkyNmE5NzZjZDdkOGE5MiJ9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Site": 'none'}
        self.initial_soup = self.get_soup(self.url)
        #self.dict_of_countries = self.get_list_of_countries()

    def get_soup(self, url):
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        print(soup)
        return soup

    def get_regions_overal(self):
        pass
