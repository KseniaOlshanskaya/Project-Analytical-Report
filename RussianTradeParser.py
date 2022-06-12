import requests
from bs4 import BeautifulSoup
import pandas as pd


class RussianTradeParser(object):
    def __init__(self):
        self.url = "https://russian-trade.com"
        self.header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "cookie": "tmr_lvid=33d9228d1d548987b75002ddd87f1a7f; tmr_lvidTS=1645202471900; _ym_uid=1645202472349136595; _ym_d=1645202472; _ga=GA1.2.1284131769.1645202472; __gads=ID=ceebec809ffd9c77-22f61b7442cd00fe:T=1645202474:RT=1645202474:S=ALNI_MYpM6Ieu9JRflEomMuEhHdpSCUhVA; bpc=c7fa671d9d9cbe966b14bb69589ce2d2; _gid=GA1.2.205493820.1649409597; _ym_isad=2; tmr_detect=0|1649410755640; tmr_reqNum=191",
    "sec-fetch-site": "cross-site", "accept-encoding": "gzip, deflate, br"}
        self.initial_soup = self.get_soup(self.url)
        self.dict_of_countries = self.get_list_of_countries()
        self.countries_links = self.get_countries_links()

    def get_soup(self, url):
        response = requests.get(url, headers=self.header)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        return soup

    def get_list_of_countries(self):
        all_countries = self.initial_soup.find(class_="country").find_all("option")
        dict_of_countries = {}
        for item in all_countries:
            dict_of_countries[item.text[:-4].strip()] = item.get("value")
        return dict_of_countries

    def get_countries_links(self):
        countries_links = {}
        for country_name in self.dict_of_countries:
            url_country = "https://russian-trade.com/countries/" + self.dict_of_countries[country_name]
            countries_links.update({country_name: url_country})
        return countries_links

    def get_soup_by_country(self, country): # Соуп по стране конкретный репорт (2021)
        url_country = "https://russian-trade.com/countries/" + self.dict_of_countries[country]
        soup = self.get_soup(url_country)
        part_url = soup.find(id="reviews-block").find("a").get("href")
        full_url = self.url + part_url

        soup = self.get_soup(full_url)
        return soup

    def get_tables(self, soup):  # Таблицы по экспорту и импорту репорта (2021)
        all_tables = soup.find_all("table", class_="report2")
        return all_tables

    def get_overal_information(self, soup):
        overal_information = []
        info = soup.find("div", class_="story-txt").find_all("p", limit=7)
        for i in info:
            i = i.text
            i = i.replace("b", "")
            i = i.replace("/b", "")
            dict_ = dict(N=i, text=i)
            overal_information.append(dict_)
            dict_ = {}
        return overal_information

    def get_product_data_frame(self, table, export=True):
        products = table.find_all("tr")
        if export:
            df = pd.DataFrame(columns=['ProductId', 'ProductName', 'ExportCurrentYear',
                                       'InAllExport', 'ExportPreviousYear', 'Change'])
        else:
            df = pd.DataFrame(columns=['ProductId', 'ProductName', 'ImportCurrentYear',
                                       'InAllImport', 'ImportPreviousYear', 'Change'])
        for row in products:
            columns = row.find_all('td')
            if (columns != []):
                if columns[0].text.strip() == "SS":
                    continue
                producId = columns[0].text.strip()
                product = columns[1].text.strip()
                export2021 = int(columns[2].text.strip().replace(" ", ""))
                inAllExport = columns[3].text.strip()
                export2020 = int(columns[4].text.strip().replace(" ", ""))
                change = columns[5].text.strip()
                group = self.get_group(int(producId))
                if export:
                    df = df.append(
                    {'ProductId': producId, 'ProductName': product,
                     'ExportCurrentYear': export2021, 'InAllExport': inAllExport,
                     'ExportPreviousYear': export2020, 'Change': change, 'Group': group},
                        ignore_index=True)
                else:
                    df = df.append(
                        {'ProductId': producId, 'ProductName': product,
                         'ImportCurrentYear': export2021, 'InAllImport': inAllExport,
                         'ImportPreviousYear': export2020, 'Change': change, 'Group': group},
                        ignore_index=True)
        return df

    @staticmethod
    def get_group(id):
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
            return "Прочие товары"