"""управленческие отчеты"""
import requests
import json
import configparser
from datetime import datetime
import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient import discovery

try:
    conf = configparser.ConfigParser()
    conf.read('reports.ini')
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
    url_profit_product = conf['MoiSklad']['url_profit_product']
    url_customer_profit_product = conf['MoiSklad']['url_customer_profit_product']
    # goggle parts
    report_book = conf['GOOGLE']['report_book']
    profit_book = conf['GOOGLE']['profit_book']
    temp_book = conf['GOOGLE']['temp_book']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
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
    def __init__(self, start_day='2021-02-08', end_day=toda_y_date):
        self.form_date = str(datetime.now().strftime("%d.%m.%y %H:%m"))
        self.start_day = start_day
        self.end_day = end_day
        self.customers_profit_dict = {}
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
            url_filtered = str(f'{url_customer_profit_product}?moment>={start_day} 00:00:00;moment<={end_day} 23:00:00') # !momentTo doesnt work
            #url_filtered = f'{url_profit_product}?momentFrom={start_day} 00:00:00;momentTo={end_day} 23:00:00')

            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            print(url_filtered)
            with open('profit_customer_list.json', 'w') as ff:
                json.dump(req.json(), ff, ensure_ascii=False)
            for elem in req.json()['rows']:
                self.customers_profit_dict[elem['counterparty']['meta']['href']] = [elem['sellSum']/100, elem['sellCostSum']/100, elem['profit']/100]
            return self.customers_profit_dict

        except IndexError:
            print('Sorry, cant get products dict ')
            return False


    def form_report(self):
        profit_by_customers_dict = self.get_profit_by_customer_list()
        data_linked = []
        for customer_link, sales in profit_by_customers_dict.items():
            customer_name = self.request_customer_data(customer_link)[0]
            customer_group = self.request_customer_data(customer_link)[1]
            data_linked.append([customer_name, customer_group, sales[0], sales[1], sales[2]])
        return data_linked



new_report = management_report(start_day='2021-03-01', end_day='2021-03-31')
new_report_book = report_book()
new_report_book.clear_data_sheet()
new_report_book.append_array(new_report.form_report())

