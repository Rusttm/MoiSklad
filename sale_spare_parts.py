""" discont on spareparts """
import configparser
import requests
import os
from datetime import date
import json
import pandas as pd
import xlsxwriter



try:
    # get data from in file
    conf = configparser.ConfigParser()
    conf.optionxform = str
    conf.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
    # эта часть кода позволяет использовать несколько заголовков
    url_headers = conf['API_HEADERS']
    headers_dict = dict()
    for header in url_headers:
        headers_dict[header] = url_headers[header]
    header_for_token_auth = headers_dict
    #
    url_customers = conf['MoiSklad']['url_customers']
    url_sales_list = conf['MoiSklad']['url_sales_list']
    url_nsk_group = conf['TAGS']['Nsk']
    url_prod_list = conf['MoiSklad']['url_prod_list']


except IndexError:
    print('Error, cant read .ini file', Exception)

agent_group_href = {'Saratov' : 'https://online.moysklad.ru/api/remap/1.2/entity/group/735e1535-570a-11eb-0a80-04f2002a960a'}

class spare_parts_check():
    def __init__(self):
        self.demands_dict = {}
        self.clients_dict = {}
        self.products_dict = {}
        self.agents_sold_spare_parts = {}

        self.work_with_demand_file()
        self.work_with_clients_file()
        self.work_with_prod_file()


    def get_positions_list(self):
        """get prod list"""
        x =[]
        y = []
        try:
            for tag_positions, [tag_demand, tag_customer] in self.demands_dict.items():
                positions_req = requests.get(url=f"{tag_positions}", headers=header_for_token_auth)
                for position in positions_req.json()['rows']:
                    prod_tag = position['assortment']['meta']['href']
                    prod_discount = position['discount']
                    if (prod_discount>0) and (prod_tag in self.products_dict.keys()):
                        customer_name = self.clients_dict[tag_customer]
                        y = self.agents_sold_spare_parts.get(customer_name, [])
                        if tag_demand not in y:
                            x = y + [tag_demand]
                        else:
                            x = y
                        self.agents_sold_spare_parts[customer_name] = x
            print(self.agents_sold_spare_parts.keys())
            print(self.agents_sold_spare_parts)
            self.write_to_file()


        except IndexError:
            print('Cant read sales data', Exception)

    def write_to_file(self):
        result_dict = self.agents_sold_spare_parts
        with xlsxwriter.Workbook('spare_parts_discount.xlsx') as workbook:
            r = 0
            # Add worksheet
            worksheet = workbook.add_worksheet()

            # Write headers
            for head, values in result_dict.items():
                worksheet.write(0, r, head)
                # Write list data
                for i, value in enumerate(values, start=1):
                    worksheet.write(i, r, value)
                r += 1


    def get_demands_list(self):
        """get demands list"""
        today = date.today()
        today_date = str(today.strftime("%d.%m.%y_%H:%M"))
        today_date_req = str(today.strftime("%Y-%m-%d"))
        failed_sales_list = []
        try:
            sales_req = requests.get(url=f"{url_otgruzka_list}", headers=header_for_token_auth)
            with open('demand_req_list.json', 'w') as ff:
                json.dump(sales_req.json(), ff, ensure_ascii=False)
        except IndexError:
            print('Cant read sales data', Exception)

    def get_clients_list(self):
        """get clients list"""
        try:
            clients_req = requests.get(url=f"{url_customers}", headers=header_for_token_auth)
            with open('clients_req_list.json', 'w') as ff:
                json.dump(clients_req.json(), ff, ensure_ascii=False)
        except IndexError:
            print('Cant read sales data', Exception)

    def get_prod_list(self):
        """get clients list"""
        try:
            clients_req = requests.get(url=f"{url_prod_list}", headers=header_for_token_auth)
            with open('prod_req_list.json', 'w') as ff:
                json.dump(clients_req.json(), ff, ensure_ascii=False)
        except IndexError:
            print('Cant read sales data', Exception)

    def work_with_demand_file(self):
        with open('demand_req_list.json', 'r') as json_data:
            d = json.load(json_data)
            for demand in d['rows']:
                tag_positions = demand['positions']['meta']['href']
                tag_group = demand['group']['meta']['href']
                tag_customer = demand['agent']['meta']['href']
                tag_demand = demand['meta']['uuidHref']
                if tag_group == url_nsk_group:
                    self.demands_dict[tag_positions] = [tag_demand, tag_customer]

    def work_with_clients_file(self):
        with open('clients_req_list.json', 'r') as json_data:
            customers = json.load(json_data)
            for customer in customers['rows']:
                tag_customer = customer['meta']['href']
                name_customer = customer['name']
                self.clients_dict[tag_customer] = name_customer


    def work_with_prod_file(self):
        with open('prod_req_list.json', 'r') as json_data:
            products = json.load(json_data)
            for prod in products['rows']:
                tag_prod = prod['meta']['href']
                name_prod = prod['name']
                full_group_name = prod['pathName']
                try:
                    prod_group_name = full_group_name.split('/')[1]
                except:
                    prod_group_name = 'unknown'
                if prod_group_name == 'Запасные части':
                    self.products_dict[tag_prod] = name_prod



x = spare_parts_check()
print(x.get_positions_list())