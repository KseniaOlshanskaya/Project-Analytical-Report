import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

url_common = "https://russian-trade.com"
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "cookie": "tmr_lvid=33d9228d1d548987b75002ddd87f1a7f; tmr_lvidTS=1645202471900; _ym_uid=1645202472349136595; _ym_d=1645202472; _ga=GA1.2.1284131769.1645202472; __gads=ID=ceebec809ffd9c77-22f61b7442cd00fe:T=1645202474:RT=1645202474:S=ALNI_MYpM6Ieu9JRflEomMuEhHdpSCUhVA; bpc=c7fa671d9d9cbe966b14bb69589ce2d2; _gid=GA1.2.205493820.1649409597; _ym_isad=2; tmr_detect=0|1649410755640; tmr_reqNum=191",
    "sec-fetch-site": "cross-site",
    "accept-encoding": "gzip, deflate, br"
}
def get_group(id):
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
    if id in [25, 26]:
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


response = requests.get(url_common, headers=header)
src = response.text
soup = BeautifulSoup(src, "lxml")


country = "Казахстан"  #input
all_countries = soup.find(class_="country").find_all("option")
dict_countries = {}
for item in all_countries:
    dict_countries[item.text[:-4].strip()] = item.get("value")


url_country = "https://russian-trade.com/countries/" + dict_countries[country]
response2 = requests.get(url_country, headers=header)
src = response2.text


soup2 = BeautifulSoup(src, "lxml")
part_url = soup2.find(id="reviews-block").find("a").get("href")
full_url = url_common + part_url

response3 = requests.get(full_url, headers=header)
src = response3.text
soup3 = BeautifulSoup(src, "lxml")

products = soup3.find_all("table", class_="report2")

info = soup3.find("div", class_="story-txt").find_all("p", limit=7)




#Работа с пандас
df = pd.DataFrame(columns=['ProductId', 'Product', 'Export2021$', 'InAllExport%', 'Export2020$', 'Change%'])
pd.set_option('display.max_columns', None)

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
        group = get_group(int(producId))

        df = df.append(
            {'ProductId': producId, 'Product': product, 'Export2021$': export2021, 'InAllExport%': inAllExport,
             'Export2020$': export2020, 'Change%': change, 'Group': group}, ignore_index=True)



dict_summ_positions = df.groupby('Group')["Export2021$"].sum().to_dict()

# Добавляем в "Прочее" значения, которые меньше чем самое большое в 500 раз
all_values_summ = sum(dict_summ_positions.values())

keys = [key for key in dict_summ_positions if dict_summ_positions.get(key)/all_values_summ < 0.03 and key != "Прочее"]
extra = [dict_summ_positions.get(key) for key in keys]

summ_extra = sum(extra) + dict_summ_positions["Прочее"]
for key in keys:
    dict_summ_positions.pop(key)

dict_summ_positions.update({"Прочее": summ_extra})

# Pie Chart
vals = dict_summ_positions.values()
labels = dict_summ_positions.keys()
plt.pie(vals)
plt.legend(labels, loc="best", bbox_to_anchor=(1,1))
plt.show()
