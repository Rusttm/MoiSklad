# -*- coding: utf8 -*-
import requests
import json
from base64 import b64encode
from datetime import datetime
from openpyxl import Workbook
import pandas as pd
from datetime import date
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
URL = conf['MoiSklad']['URL']
URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
alex_access_token = conf['MoiSklad']['alex_access_token']
header_for_token_auth = {'Authorization': 'Bearer %s' % alex_access_token}

url_customers = conf['MoiSklad']['url_customers']





def auth_api():
    ''''get token from for api'''
    logpass=str.encode(conf['MoiSklad']['alex_log_pass'])
    userAndPass = b64encode(logpass).decode("ascii") #b"user@outlook.com:12345"
    headers = { 'Authorization': 'Basic %s' % userAndPass }
    req = requests.get(url=URL, headers=headers)  # вариант обычного запроса
    f = open("msanswer.html", "w+")
    f.write(req.text)
    f.close()
    token_req = requests.post(url=URL_TOKEN, headers=headers)  # получаем токен
    return token_req.text

def get_customers_list():
    '''Return customer name'''
    try:
        req=requests.get(url=url_customers, headers=header_for_token_auth)
        with open('alex_customer_list.json', 'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        return req.json()['name']
    except Exception:
        print('Sorry, cant get customers list ', Exception)
        return False

def get_otgruzka_list():
    '''get sales list in file .json'''
    try:

        data_linked=[]
        req=requests.get(url=url_otgruzka_list, headers=header_for_token_auth)
        toda_y=str(datetime.now().strftime("%Y_%m_%d"))
        list_date=datetime.now().date()
        list_date_format=list_date.strftime("%d.%m.%y")
        file_name = str('alex_sales_%s.json' % toda_y)
        with open(file_name,'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        for demand in req.json()['rows']:
            demand_doc = str(demand['meta']['uuidHref'])
            demand_no = demand['name']
            demand_date = datetime.strptime(str(demand['moment']),"%Y-%m-%d %H:%M:%S.%f").date()
            demand_no_date=str(f'№ {demand_no} от {demand_date}')
            time_delta = list_date-demand_date
            time_delta_days = time_delta.days
            demand_sum = int(demand['sum'])/100
            demand_payed_sum = demand['payedSum']/100
            difference = demand_sum - demand_payed_sum
            if int(demand['sum']) == int(demand['payedSum']):
                payed = True
            else:
                payed = False
                customer_link = demand['agent']['meta']['href']
                customer_data = get_customer_name(customer_link)
                customer_name = customer_data['name']
                customer_tags_list = customer_data['tags_list']
                customer_shift_days = customer_data['shift_days'] #отсрочка клиента дней
                remains = int(customer_shift_days) - int(time_delta_days)
                if  remains < 0 : customer_debt='Просрочено!'
                else: customer_debt = 'В рамках отсрочки'

                    #print(f'Отгрузка № {demand_no} от {demand_date} на сумму {demand_sum} руб. {customer_name} отсрочка {customer_shift_days} не оплачено {difference}')
                data_linked.append([list_date_format, customer_tags_list,customer_name,demand_no_date,demand_doc,customer_shift_days,remains,difference,customer_debt])
        fill_the_df(data_linked)
        return True
    except Exception:
        print('Error, cant get sales list', Exception)
        return False

def get_customer_name(customer_href):
    '''Return customer name'''
    shift_days_values = 0
    tags = []
    try:
        customer_req = requests.get(url=customer_href, headers=header_for_token_auth)
        name_customer = customer_req.json()['name']
        try:

            for tag in customer_req.json()['tags']:
                tags.append(tag)
            tags_str=', '.join([str(elem) for elem in tags])
        except Exception:
            print('Error, there are no tags in list', Exception)

        try:
            b = customer_req.json()['attributes']
            #c = b['0']
            d = b[0]['value']
            shift_days_values = d
        except Exception:
            print(f'Error, there are no attributes in list {customer_href}', Exception)

        x={'name':customer_req.json()['name'], 'tags_list': tags_str, 'shift_days': shift_days_values}
        return x
    except Exception:
        print('Error, cant find customer', Exception)
        y = {'name':'Unknown_Customer','tags_list': tags, 'shift_days':shift_days_values}
        return y
def fill_the_df(data_linked):
    try:
        columns_for_df = ['Дата формирования отчета', 'Группы покупателя', 'Покупатель', 'Номер и дата отгрузки',
                          'ссылка на документ', 'Отсрочка, дней', 'Дней до оплаты', 'Размер просроченной задолженности', 'Статус']
        df_sales = pd.DataFrame(columns=columns_for_df)
        df_sales = df_sales.append(pd.DataFrame(data_linked, columns=columns_for_df), ignore_index=True)
        df_sales.sort_values(by=['Группы покупателя', 'Покупатель'], inplace=True)
        #print(df_sales)
        '''write to excell'''
        try:
            today = date.today()
            sheet_name = str(today.strftime("%m-%d-%y"))
            with pd.ExcelWriter('alex_debt_%s.xlsx' % today) as writer:
                df_sales.to_excel(writer, index=False, sheet_name=sheet_name)
        except Exception:
            print('Error, cant create file', Exception)

    except Exception:
        print('Error cant fill the DataFrame', Exception)


get_otgruzka_list()
