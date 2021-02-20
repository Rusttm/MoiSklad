# -*- coding: utf8 -*-
import requests
import json
from base64 import b64encode
from datetime import datetime
import xlsxwriter
from datetime import date
import configparser


conf = configparser.ConfigParser()
conf.read('alex.ini')
URL = conf['MoiSklad']['URL']
URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
alex_access_token = conf['MoiSklad']['alex_access_token']
header_for_token_auth = {'Authorization': 'Bearer %s' % alex_access_token}
url_customers = conf['MoiSklad']['url_customers']


def auth_api():
    """get token from for api"""
    logpass = str.encode(conf['MoiSklad']['alex_log_pass'])
    userAndPass = b64encode(logpass).decode("ascii")  # b"user@outlook.com:12345"
    headers = {'Authorization': 'Basic %s' % userAndPass}
    req = requests.get(url=URL, headers=headers)  # вариант обычного запроса
    f = open("msanswer.html", "w+")
    f.write(req.text)
    f.close()
    token_req = requests.post(url=URL_TOKEN, headers=headers)  # получаем токен
    return token_req.text


def get_customers_list():
    """'''Return customer name'''"""
    try:
        req = requests.get(url=url_customers, headers=header_for_token_auth)
        with open('alex_customer_list.json', 'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        return req.json()['name']

    except IndexError:
        print('Sorry, cant get customers list ')
        return False


def fill_the_df(data_linked):
    try:
        columns_for_df = ['Дата формирования отчета', 'Группы покупателя', 'Покупатель',
                          'Номер и дата отгрузки', 'Отсрочка, дней', 'Дней до оплаты',
                          'Размер просроченной задолженности', 'Статус', 'ссылка на документ']
        '''write to excell'''
        data_linked = sorted(data_linked, key=lambda y: (y[1], y[2], y[3]))  # sorting by group and name
        try:
            today = date.today()
            file_date = str(today.strftime("%d.%m.%y"))
            file_name = str('alex_debt_%s.xlsx' % today)
            alex_workbook = xlsxwriter.Workbook(file_name)
            alex_worksheet = alex_workbook.add_worksheet(str(today.strftime("%d-%m-%y")))
            bold = alex_workbook.add_format({'bold': True})

            # insert top line
            for col_num, col_data in enumerate(columns_for_df):
                alex_worksheet.write(0, col_num, col_data, bold)

            customer_name = 'Покупатель'
            start_row = 1
            shift_row = 1  # shifting for write total sum
            doc_sum = 0
            row_num = 0
            # write data to file and insert Total sums
            for row_num, row_data in enumerate(data_linked):
                new_customer_name = row_data[2]
                doc_sum += float(row_data[6])
                if not ((customer_name == new_customer_name) or (customer_name == 'Покупатель')):
                    alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 0})
                    alex_worksheet.write(row_num + shift_row, 0, customer_name, bold)
                    alex_worksheet.write(row_num + shift_row, 5, 'Всего', bold)
                    alex_worksheet.write(row_num + shift_row, 6, f'=SUM(G{start_row}:G{row_num+ shift_row})', bold)
                    shift_row += 1
                    start_row = row_num + shift_row + 1
                alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 1})
                for col_num, col_data in enumerate(row_data):
                    alex_worksheet.write(row_num + shift_row, col_num, col_data)
                customer_name = new_customer_name
            '''make last customer summary'''
            alex_worksheet.write(row_num + shift_row+1, 0, customer_name, bold)
            alex_worksheet.write(row_num + shift_row+1, 5, 'Всего', bold)
            alex_worksheet.write(row_num + shift_row+1, 6, f'=SUM(G{start_row}:G{row_num + shift_row+1})', bold)

            '''make all customer summary'''
            alex_worksheet.write(row_num + shift_row+2, 0, 'По всем клиентам', bold)
            alex_worksheet.write(row_num + shift_row+2, 2, doc_sum, bold)
            alex_workbook.close()
            return [file_name, round(doc_sum, 2), file_date]
        except IndexError:
            print('Error, cant create file', Exception)
            return [False, False, False]
    except IndexError:
        print('Error cant fill the DataFrame', Exception)
        return [False, False, False]


def get_otgruzka_list():
    """'''get sales list in file .json'''"""
    try:

        data_linked = []
        req = requests.get(url=url_otgruzka_list, headers=header_for_token_auth)
        toda_y = str(datetime.now().strftime("%Y_%m_%d"))
        list_date = datetime.now().date()
        list_date_format = list_date.strftime("%d.%m.%y")
        file_name = str('alex_sales_%s.json' % toda_y)
        with open(file_name, 'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        for demand in req.json()['rows']:
            demand_doc = str(demand['meta']['uuidHref'])
            demand_no = demand['name']
            demand_date = datetime.strptime(str(demand['moment']), "%Y-%m-%d %H:%M:%S.%f").date()
            demand_no_date = str(f'№ {demand_no} от {demand_date}')
            time_delta = list_date-demand_date
            time_delta_days = time_delta.days
            demand_sum = int(demand['sum'])/100
            demand_payed_sum = demand['payedSum']/100
            difference = demand_sum - demand_payed_sum
            if int(demand['sum']) != int(demand['payedSum']):  # fill only unpaid sales
                customer_link = demand['agent']['meta']['href']
                customer_data = get_customer_name(customer_link)
                customer_name = customer_data['name']
                customer_tags_list = customer_data['tags_list']
                customer_shift_days = customer_data['shift_days']  # отсрочка клиента дней
                remains = int(customer_shift_days) - int(time_delta_days)
                if remains < 0:
                    customer_debt = 'Просрочено!'
                else:
                    customer_debt = 'В рамках отсрочки'
                data_linked.append([list_date_format, customer_tags_list, customer_name,
                                    demand_no_date, customer_shift_days, remains,
                                    difference, customer_debt, demand_doc])

        return fill_the_df(data_linked)
    except IndexError:
        print('Error, cant get sales list', Exception)
        return [False, False, False]


def get_customer_name(customer_href):
    """'''Return customer name'''"""
    shift_days_values = 0
    tags = []
    try:
        customer_req = requests.get(url=customer_href, headers=header_for_token_auth)
        try:

            for tag in customer_req.json()['tags']:
                tags.append(tag)
            if len(tags) == 0:
                tags_str = 'Серман'
            else:
                tags_str = ', '.join([str(elem) for elem in tags])
        except IndexError:
            print('Error, there are no tags in list', Exception)

        try:
            b = customer_req.json()['attributes']
            d = b[0]['value']
            shift_days_values = d
        except IndexError:
            print(f'Error, there are no attributes in list {customer_href}', Exception)

        x = {'name': customer_req.json()['name'], 'tags_list': tags_str, 'shift_days': shift_days_values}
        return x
    except IndexError:
        print('Error, cant find customer', Exception)
        y = {'name': 'Unknown_Customer', 'tags_list': tags, 'shift_days': shift_days_values}
        return y
