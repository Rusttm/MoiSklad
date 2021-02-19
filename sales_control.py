import configparser
from math import ceil, floor
import pathlib
import requests
from datetime import date
import json


try:
    #get data from in file
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
    url_customers = conf['MoiSklad']['url_customers']
except:
    print('Error, cant read .ini file')


today = date.today()
today_date = str(today.strftime("%d.%m.%y_%H:%M"))
today_date_req = str(today.strftime("%Y-%m-%d"))

def round_number(numb: float):
    x=(numb*10000)//100
    return x

def get_sales_list():
    try:
        failed_sales_list = []
        #, filter = date > '2021-02-08 12:00:00'
        #sales_req = requests.get(url=f'{url_sales_list}?filter=number=100', headers=header_for_token_auth)
        sales_req = requests.get(url=f"https://online.moysklad.ru/api/remap/1.2/report/profit/bycounterparty?momentFrom={today_date_req} 00:00:01", headers=header_for_token_auth)
        #with open('sales_req_list.json', 'w') as ff:
        #    json.dump(sales_req.json(), ff, ensure_ascii=False)
        for client in sales_req.json()['rows']:
            client_name=client['counterparty']['name']
            client_sales=round(client['sellSum']/100,2)
            client_profit = client['profit']/100
            client_rent=round_number(client_profit/client_sales)
            if client_rent < 30:
                failed_sales_list.append([client_name, client_sales, client_rent])
        return failed_sales_list
    except Exception:
        print('Cant read sales data', Exception)
        return failed_sales_list
