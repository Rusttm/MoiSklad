"""управленческие отчеты"""
import requests
import json
import configparser
from datetime import datetime
import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from googleapiclient import discovery

try:
    conf = configparser.ConfigParser()
    #conf.read('reports.ini')
    conf.read(os.path.join(os.path.dirname(__file__), 'config/reports.ini'))
except IndexError:
    print('cant find .ini file'), Exception


try:
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % access_token}
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_customers = conf['MoiSklad']['url_customers']
    url_payments_list = conf['MoiSklad']['url_payments_list']
    url_outpayments_list = conf['MoiSklad']['url_outpayments_list']
    url_profit_product = conf['MoiSklad']['url_profit_product']
    url_customer_profit_product = conf['MoiSklad']['url_customer_profit_product']
    # goggle parts
    report_book = conf['GOOGLE']['report_book']
    profit_book = conf['GOOGLE']['profit_book']
    temp_book = conf['GOOGLE']['temp_book']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
    CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILE)
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # print(f'Googgle book https://docs.google.com/spreadsheets/d/{report_book}/edit#gid=0 initiated')
except IndexError:
    print('cant load data from .ini file', Exception)


try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build(API_SERVICE_NAME, API_VERSION, http=httpAuth,
                                        cache_discovery=False)  # Выбираем работу с таблицами и 4 версию API
except IndexError:
    print('Cant run google api', Exception)
    exit(1)

toda_y_date = str(datetime.now().strftime("%Y-%m-%d"))

class report_book():
    def __init__(self):
        self.bookName = 'Отчеты управленческие'
        self.email = 'rustammazhatov@gmail.com'
        self.bookId = profit_book
        self.today_date = str(datetime.now().strftime("%Y%m%d"))
        self.sheets = []
        self.sheets_dict = {}

    def get_sheets_list(self, book_Id = profit_book):
        try:
            request = service.spreadsheets().get(spreadsheetId = book_Id)
            spreadsheet =  request.execute()
            sheetList = spreadsheet.get(API_SERVICE_NAME)
            for sheet in sheetList:
                self.sheets.append([sheet['properties']['sheetId'], sheet['properties']['title']])
            return self.sheets
        except IndexError:
            print(f'Cant get sheet list of the book', Exception)
            return [False, False]

    def get_sheets_dict(self):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=self.bookId).execute()
            sheetList = spreadsheet.get(API_SERVICE_NAME)
            for sheet in sheetList:
                self.sheets_dict[str(sheet['properties']['sheetId'])] = str(sheet['properties']['title'])
                self.sheets_dict[str(sheet['properties']['title'])] = str(sheet['properties']['sheetId'])
            return self.sheets_dict
        except IndexError:
            print(f'Cant get sheet list of the book', Exception)
            return {"0": "NONAME"}

    def get_sheet_name(self, sheetid = 0):
        try:
            a = self.get_sheets_dict()[str(sheetid)]
            return a
        except IndexError:
            print(f'Cant get sheet name in the book', Exception)
            return 'noname'

    def make_new_sheet(self, new_sheet_name=toda_y_date):
        try:
            got_list = self.get_sheets_list()
            got_list = sorted(got_list, key=lambda y: (y[0], y[1]))
            new_sheet_id = got_list[-1][0] + 1  # find last id
            got_sheet_names = [x[1] for x in got_list]  # make list of sheets
            shift = 0
            # resolve sheet names conflict by adding _0 _1 _2 _3
            while new_sheet_name in got_sheet_names:
                new_sheet_name = f"{new_sheet_name}_{shift}"
                shift += 1
            request_body = {
                "requests": [{
                    "addSheet": {
                        "properties": {
                            "sheetId": new_sheet_id,
                            "title": new_sheet_name,
                            "tabColor": {
                                "red": 0.01,
                                "green": 0.9,
                                "blue": 0.9
                            }
                        }
                    }
                }]}
            new_sheet_req = service.spreadsheets().batchUpdate(
                spreadsheetId=self.bookId,
                body=request_body).execute()
            return [new_sheet_id, new_sheet_name]
        except IndexError:
            print('Cant make new sheet in the book', Exception)
            return [False, False]

    def give_access_to_book(self, user_mail = 'rustammazhatov@gmail.com'):
        try:
            # Выбираем работу с Google Drive и 3 версию API
            drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
            access = drive_service.permissions().create(
                fileId = self.bookId, body = {'type': 'user', 'role': 'writer', 'emailAddress': user_mail},
                fields = 'id').execute() # Открываем доступ на редактирование
            return True
        except IndexError:
            print(f'Cant create accsess for {self.email} to the book', Exception)
            return False

    def clear_data_sheet(self, sheetid = 0, clear_range='A1:M1000'):
        try:
            sheetName = self.get_sheet_name(sheetid)
            rangeAll = '{0}!A1:Z'.format(sheetName)
            work_book = self.bookId
            request = service.spreadsheets().values().clear(spreadsheetId=work_book, range=rangeAll, body={})
            response = request.execute()
            return response
        except IndexError:
            print(f'Cant clear {sheetid} sheet', Exception)
            return Exception

    def append_array(self, work_array, sheetid=0):
        try:
            sheetName = self.get_sheet_name(sheetid)
            rangeAll = '{0}!A1:M1000'.format(sheetName)
            values =  {'values' : work_array}
            result = service.spreadsheets().values().append(
                spreadsheetId=self.bookId, range=rangeAll,
                valueInputOption='RAW',
                body=values).execute()
            return result
        except IndexError:
            print('Cant append array to the book', Exception)
            return Exception


class management_report():
    def __init__(self, start_day='2021-02-08', end_day=str(datetime.now().strftime("%Y-%m-%d"))):
        self.form_date = str(datetime.now().strftime("%d.%m.%y %H:%m"))
        self.start_day = start_day
        self.end_day = end_day
        self.customers_profit_dict = {}
        self.outpayments_purpose_dict = {}
        self.general_profit = 0
        #print('today is', toda_y_date)

    def request_customer_data(self, customer_link):
        """return data from facture return [customer_name, customer_group]"""
        try:
            customer_req = requests.get(url=customer_link, headers=header_for_token_auth)
            customer = customer_req.json()
            group_request = requests.get(url=customer['group']['meta']['href'], headers=header_for_token_auth)
            customer_group = group_request.json()['name']
            customer_data_list = [customer['name'], customer_group]
            return customer_data_list
        except IndexError:
            print(f'Error, cant find the customer {customer_link}', Exception)

    def get_profit_by_customer_list(self):
        """'''Return dict { prod_link : sale_cost}'''"""
        #start_day_for_sales =  self.start_day
        end_day = self.end_day
        start_day = self.start_day
        try:
            #url_filtered = str(f'{url_customer_profit_product}?moment>={start_day} 00:00:00;moment<={end_day} 23:00:00') # !momentTo doesnt work
            url_filtered = f'{url_customer_profit_product}?momentFrom={start_day} 00:00:00&momentTo={end_day} 23:00:00'
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            with open('profit_customer_list.json', 'w') as ff:
                json.dump(req.json(), ff, ensure_ascii=False)
            for elem in req.json()['rows']:
                self.customers_profit_dict[elem['counterparty']['meta']['href']] = [elem['sellSum']/100, elem['sellCostSum']/100, elem['profit']/100]
            return self.customers_profit_dict

        except IndexError:
            print('Sorry, cant get products dict ')
            return False

    def get_payments_by_purpose_list(self):
        """returns dict {paymentPurpose: paymentSum}"""
        data_linked2 = []
        temp_dict = {}
        #url_filtered = f'{url_outpayments_list}?momentFrom={self.start_day} 00:00:00&momentTo={self.end_day} 23:00:00'
        url_filtered = f'{url_outpayments_list}?filter=created>={self.start_day} 00:00:00;created<={self.end_day} 23:00:00'
        req = requests.get(url=url_filtered, headers=header_for_token_auth)
        #with open('outpayments_list.json', 'w') as ff:
        #    json.dump(req.json(), ff, ensure_ascii=False)
        # fill dictt by data
        for elem in req.json()['rows']:
            temp_dict[elem['expenseItem']['meta']['href']] = temp_dict.get(elem['expenseItem']['meta']['href'], 0) + elem['sum']
        # convert link to names
        for key, value in temp_dict.items():
            req2 = requests.get(url=key, headers=header_for_token_auth)
            req2.json()['name']
            self.outpayments_purpose_dict[req2.json()['name']] = value
            data_linked2.append([req2.json()['name'], value])

        return self.outpayments_purpose_dict

    def form_profit_by_customers_report(self):
        """ main module for profit list"""
        # this dict return group:[sumsales,sumcost,sumprofit]
        profits_by_group_dict = {'Наименование': ['Выручка', 'Себестоимость', 'Валовая прибыль'],
                                 'Всего': [0, 0, 0],
                                 'Новосибирск': [0, 0, 0],
                                 'Саратов': [0, 0, 0],
                                 'Москва': [0, 0, 0],
                                 'Основной': [0, 0, 0]}
        profit_by_customers_dict = self.get_profit_by_customer_list()
        data_linked = [['отчет создан:', self.form_date], ['период с:', self.start_day], ['период по:', self.end_day],[]]
        for customer_link, sales in profit_by_customers_dict.items():
            customer_name = self.request_customer_data(customer_link)[0]
            customer_group = self.request_customer_data(customer_link)[1]
            try:
                profits_by_group_dict[customer_group][0] += sales[0]
                profits_by_group_dict[customer_group][1] += sales[1]
                profits_by_group_dict[customer_group][2] += sales[2]
                profits_by_group_dict['Всего'][0] += sales[0]
                profits_by_group_dict['Всего'][1] += sales[1]
                profits_by_group_dict['Всего'][2] += sales[2]

            except:
                print(f'Cant find new group {customer_group} in dictionary')
        # make the dataframe
        my_df = pd.DataFrame(profits_by_group_dict)
        data_linked.append(list(profits_by_group_dict.keys()))
        for strin_g in my_df.values.tolist():
            data_linked.append(strin_g)
        #data_linked.append([customer_name, customer_group, sales[0], sales[1], sales[2]])
        #data_linked = sorted(data_linked, key = lambda s: (s[1]))
        return data_linked

    def form_general_report(self):
        dropped_purpose = ['Выплаты Агенту', 'Закупка товаров', 'Перемещение', 'Чистая прибыль', 'Операционная прибыль', 'Операционные расходы']
        data_linked_list = self.form_profit_by_customers_report()
        temp_dict = self.get_payments_by_purpose_list()
        temp_dict['Чистая прибыль'] = data_linked_list[-1][1]
        nsk_profit = (data_linked_list[-1][2] - temp_dict.get('Новосибирск склад', 0)/100)*0.8*0.35
        pfo_profit = (data_linked_list[-1][3] - temp_dict.get('Саратов склад', 0)/100)*0.8*0.5*0 # exclude from 17-05-21
        data_linked_list.append(['Выплаты Агенту', nsk_profit+pfo_profit, nsk_profit, pfo_profit ])
        temp_dict['Чистая прибыль'] -= nsk_profit + pfo_profit
        for key, value in temp_dict.items():
            if key not in dropped_purpose:
                temp_dict['Чистая прибыль'] -= value/100
                data_linked_list.append([key, value/100])
        data_linked_list.append(['Чистая прибыль', temp_dict['Чистая прибыль']])
        self.general_profit = temp_dict['Чистая прибыль']
        return data_linked_list

def monthly_report(start_day='2021-05-01', end_day='2021-05-31'):
    new_report = management_report(start_day=start_day, end_day=end_day)
    new_report_book = report_book()
    new_report_book.clear_data_sheet()
    new_report_book.append_array(new_report.form_general_report())
    return profit_book

def actual_report():
    toda_y_date = str(datetime.now().strftime("%Y-%m-%d"))
    todayYear = datetime.now().year
    todayMonth = datetime.now().month
    new_report = management_report(start_day=f'{todayYear}-{todayMonth}-01', end_day=toda_y_date)
    new_report_book = report_book()
    new_report_book.clear_data_sheet()
    new_report_book.append_array(new_report.form_general_report())
    report_link = f'https://docs.google.com/spreadsheets/d/{profit_book}/edit#gid=0'
    generalProfit = new_report.general_profit
    return (int(generalProfit), report_link)


#print(new_report.get_payments_by_purpose_list())
