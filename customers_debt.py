# -*- coding: utf8 -*-
import requests
import json
from base64 import b64encode
from datetime import datetime
import xlsxwriter
from datetime import date
import configparser
import google_books
import os

conf = configparser.ConfigParser()
conf.optionxform = str

conf.read(os.path.join(os.path.dirname(__file__), 'config/c_debdt.ini'))
access_token = conf['MoiSklad']['access_token']
header_for_token_auth = {'Authorization': 'Bearer %s' % access_token}
# эта часть кода позволяет использовать несколько заголовков
url_headers = conf['API_HEADERS']
headers_dict = dict()
for header in url_headers:
    headers_dict[header] = url_headers[header]
header_for_token_auth = headers_dict
#
url_customers = conf['MoiSklad']['url_customers']


def get_customer_tag(link='https://online.moysklad.ru/api/remap/1.2/entity/counterparty/aea8eed7-5738-11eb-0a80-06ec00ac6c64'):
    """gets link and returns tag"""
    try:
        req = requests.get(url=link, headers=header_for_token_auth)
        return req.json()['tags'][0]
    except IndexError:
        print('Error, cant get customer group tag ', Exception)
        return False


def get_customers_balance():
    """'''Return customers debt grouped by branches'''"""
    sales_group_customers = {'новосибирскконтрагенты': 0, 'покупатели пфо': 0, 'москваконтрагенты':0, 'покупатели': 0, 'Итого': 0}
    support_group_customers = {'офис поставщики': 0, 'транспорт': 0, 'поставщики': 0, 'Итого': 0}

    try:
        filtered_url = f'{url_customers}?filter=balance<0'
        req = requests.get(url=filtered_url, headers=header_for_token_auth)
        #with open('customer_balance_list.json', 'w') as ff:
        #    json.dump(req.json(), ff, ensure_ascii=False)
        for row in req.json()['rows']:
            group_tags = get_customer_tag(row['counterparty']['meta']['href'])
            customer_balance = row['balance']/100
            if group_tags in sales_group_customers:
                sales_group_customers[group_tags] += customer_balance
                sales_group_customers['Итого'] += customer_balance
            elif  group_tags in support_group_customers:
                support_group_customers[group_tags] += customer_balance
                support_group_customers['Итого'] += customer_balance
        print('Formed customers balance list ')
    except IndexError:
        print('Sorry, cant get customers balance list ')


    return {'Покупатели': sales_group_customers, 'Поставщики': support_group_customers}
