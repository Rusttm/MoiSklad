# -*- coding: cp1251 -*-
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import pars_sites
import xlsxwriter


def test1():
    url='https://www.pakt-group.ru/catalog/skobi/c1092/?page=2&next=21&lang=ru&webp=1'
    http = urllib3.PoolManager()
    fields = {'page': 2}
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
             'page': 2}
    response= http.request('GET', url, fields=fields, headers=headers)
    soup = BeautifulSoup(response.data, 'lxml')
    quotes_names_block = soup.find_all('div', class_='catalog-model-name catalog-list-tile-name')
    print(len(quotes_names_block), response.status, response.data, response.headers)

x = {'ООО "ИНТЕР-ТРЕЙД"': ['https://online.moysklad.ru/app/#demand/edit?id=2174c35f-cd9d-11eb-0a80-000a0030abd9', 'https://online.moysklad.ru/app/#demand/edit?id=2437c630-ad82-11eb-0a80-014f00081aee', 'https://online.moysklad.ru/app/#demand/edit?id=76781a13-cda0-11eb-0a80-051e00311358', 'https://online.moysklad.ru/app/#demand/edit?id=c056a4c0-7021-11eb-0a80-052c00043846', 'https://online.moysklad.ru/app/#demand/edit?id=d69f1f51-a319-11eb-0a80-06850002042b', 'https://online.moysklad.ru/app/#demand/edit?id=edb8e8ed-8604-11eb-0a80-0470003c8aa1'], 'ООО "МТ-СИБИРЬ"': ['https://online.moysklad.ru/app/#demand/edit?id=2d1c1eb3-9c3a-11eb-0a80-008800097d4a'], 'ООО ПТК "АСКО"': ['https://online.moysklad.ru/app/#demand/edit?id=7280e678-6cd7-11eb-0a80-07710001f8fd', 'https://online.moysklad.ru/app/#demand/edit?id=7c16c19d-9c38-11eb-0a80-032000093dee'], 'ООО "ПАЛЛЕТ СЕРВИС"': ['https://online.moysklad.ru/app/#demand/edit?id=98b21e1c-7805-11eb-0a80-06660003c2b4'], 'ООО "КРАСДИВАН"': ['https://online.moysklad.ru/app/#demand/edit?id=d8f646e6-e2ef-11eb-0a80-04a400287d5c'], 'ООО "ЭГИДА-СИБИРЬ"': ['https://online.moysklad.ru/app/#demand/edit?id=eb620f65-9815-11eb-0a80-0d3100016f06']}


def write_df():
    with xlsxwriter.Workbook('spare_parts_discount.xlsx') as workbook:
        r=0
        # Add worksheet
        worksheet = workbook.add_worksheet()

        # Write headers
        for head, values in x.items():
            worksheet.write(0, r, head)
            # Write list data
            for i, value in enumerate(values, start=1):
                worksheet.write(i, r, value)
            r += 1



write_df()

