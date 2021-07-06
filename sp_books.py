# -*- coding: utf8 -*-
"""this module is for sales and purchases books forms"""
import requests
import json
import configparser
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

try:
    conf = configparser.ConfigParser()
    #conf.read('sp_books.ini')
    conf.read(os.path.join(os.path.dirname(__file__), 'config/sp_books.ini'))
except IndexError:
    print('cant find .ini file'), Exception

try:
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % access_token}
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_priemka_list = conf['MoiSklad']['url_priemka_list']
    url_customers = conf['MoiSklad']['url_customers']
    url_factureout_list = conf['MoiSklad']['url_factureout_list']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE_MACOS']
    CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILE)
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    work_book = conf['GOOGLE']['work_book']
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

toda_y_date = str(datetime.now().strftime("%Y-%m-%d"))


class sp_books():
    """new class for sales and purchases books"""
    def __init__(self, start_day='2021-02-08', end_day='2021-02-28'):
        self.start_day = start_day
        self.end_day = end_day
        self.bookId = work_book
        self.bookName = 'Книги продаж и покупок'
        self.email = 'rustammazhatov@gmail.com'
        self.sheets = []
        self.sheets_dict = {}
        self.today_date = str(datetime.now().strftime("%Y%m%d"))

    def get_sheets_list(self):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=self.bookId).execute()
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
            return {"0":"NONAME"}

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

    def clear_data_sheet(self, sheetid = 0, clear_range='A1:M1000'):
        try:
            sheetName = self.get_sheet_name(sheetid)
            rangeAll = '{0}!A1:Z'.format(sheetName)
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


class moi_sklad():
    def __init__(self, start_day='2021-02-08', end_day=toda_y_date):
        self.start_day = start_day
        self.end_day = end_day
        self.sales_arr=[['№ п/п', 'Дата сф', 'Номер сф',
                        'Наименование покупателя', 'ИНН покупателя', 'Наименование и код валюты',
                         'Стоимость продажи с НДС', 'Сумма НДС 20%'],
                        ['1', '2', '3', '4', '5', '6', '7', '8']]
        self.purchase_arr=[['№ п/п', 'Дата сф продавца', 'Номер вх документа',
                            'Наименование покупателя', 'ИНН покупателя', 'Наименование и код валюты',
                            'Стоимость продажи с НДС', 'Сумма НДС 20%'],
                           ['1', '2', '3', '4', '5', '6', '7', '8']]

    def get_factureout_list(self, start_day='2021-02-08', end_day=toda_y_date):
        """'''get factures out  list from MS and put it in file .json'''"""
        try:
            data_linked = []
            url_filtered = str(
                f'{url_factureout_list}?filter=moment>={start_day} 00:00:00.000;moment<={end_day} 00:00:00.000')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            self.req_date = str(datetime.now().strftime("%Y_%m_%d"))
            self.start_day = start_day
            self.end_day = end_day
            file_name = str('factureout_book_%s.json' % self.req_date)
            with open(file_name, 'w') as ff:
                json.dump(req.json(), ff, ensure_ascii=False)
            self.f_out_json = req.json()
            """prepare data in list format"""
            try:
                print('Ok')
            except IndexError:
                print('Error, cant prepare array for sales book ', Exception)

            return True
        except IndexError:
            print('Error, cant get sales list from MS', Exception)
            return [['MS error' for _ in range(11)]]

    def request_facture_data(self, facture_link):
        """return data from facture """
        try:
            req = requests.get(url=facture_link, headers=header_for_token_auth)
            f_data = req.json()
            f_date_moment = str(f_data['moment'])
            f_date = datetime.strptime(f_date_moment,'%Y-%m-%d %H:%M:%S.%f').date()
            facture_data_list = [f_data['name'], str(f_date), f_data['sum']]
            return facture_data_list
        except:
            return ['б/н', 'неизвестно', '0']

    def request_facturein_data(self, facture_link):
        """return data from facture """
        try:
            req = requests.get(url=facture_link, headers=header_for_token_auth)
            f_data = req.json()
            f_date_moment = str(f_data['incomingDate'])
            f_date = datetime.strptime(f_date_moment, '%Y-%m-%d %H:%M:%S.%f').date()
            f_date1 = f_date.strftime("%d.%m.%y")
            facture_data_list = [f_data['incomingNumber'], str(f_date1), f_data['sum']]
            return facture_data_list
        except:
            return ['б/н', 'неизвестно', '0']

    def request_customer_data(self, customer_link):
        """return data from facture """
        try:
            customer_req = requests.get(url=customer_link, headers=header_for_token_auth)
            customer = customer_req.json()
            customer_data_list = [customer['name'], customer['inn']]
            return customer_data_list
        except IndexError:
            print(f'Error, cant find the customer {customer_link}', Exception)

            #return ['неизвестно', 'неизвестно']

    def get_sales_list(self, start_day='2021-02-08', end_day=toda_y_date):
        """'''get sales list from MS and put it in file .json'''"""
        data_linked = []
        doc_sum = 0
        vatsum = 0
        position = 0
        try:
            url_filtered = str(
                f'{url_otgruzka_list}?order=moment,name&filter=moment>={start_day} 00:00:00.000;moment<={end_day} 23:00:00.000')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            self.req_date = str(datetime.now().strftime("%Y_%m_%d"))
            self.start_day = start_day
            self.end_day = end_day
            #file_name = str('sales_book_%s.json' % self.req_date)
            #with open(file_name, 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)

            """prepare data in list format"""
            try:
                sales_json = req.json()
                for sale in sales_json['rows']:
                    sale_date_0 = datetime.strptime(str(sale['moment']),'%Y-%m-%d %H:%M:%S.%f').date()
                    sale_date = sale_date_0.strftime("%d.%m.%y")
                    sale_name = sale['name']
                    sale_sum = sale['sum']/100
                    if sale['vatEnabled']: sale_vat = sale['vatSum']/100
                    else: sale_vat = 0

                    try:
                        f_out_link = sale['factureOut']['meta']['href']
                        facture_data = self.request_facture_data(f_out_link)
                    except:
                        continue
                        facture_data = ['б/н', 'неизвестно', '0']

                    try:
                        customer_link = sale['agent']['meta']['href']
                        customer_data = self.request_customer_data(customer_link)
                    except:
                        continue
                        customer_data = ['неизвестно', 'неизвестно']

                    position += 1
                    doc_sum += sale_sum
                    vatsum += sale_vat
                    data_linked.append([position, sale_date, facture_data[0],
                                        customer_data[0], customer_data[1], 'Российский рубль,643',
                                        sale_sum, sale_vat])
            except IndexError:
                print('Error, cant prepare array for sales book ', Exception)

        except IndexError:
            print('Error, cant get sales list from MS', Exception)

        #data_linked = sorted(data_linked, key=lambda y: (y[1], y[4], y[2]))  # sorting by group and name
        data_linked = self.sales_arr + data_linked
        data_linked.append(['', '', '',
                            '', '', '',
                            doc_sum, vatsum])
        return data_linked

    def get_purchases_list(self, start_day='2021-02-08', end_day=toda_y_date):
        """'''get purchases list from MS and put it in file .json'''"""
        data_linked = []
        doc_sum = 0
        vatsum = 0
        position = 0
        try:
            url_filtered = str(
                f'{url_priemka_list}?order=moment,name&filter=moment>={start_day} 00:00:00.000;moment<={end_day} 23:00:00.000')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            self.req_date = str(datetime.now().strftime("%Y_%m_%d"))
            self.start_day = start_day
            self.end_day = end_day
            file_name = str('supply_book_%s.json' % self.req_date)
            #with open(file_name, 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)

            """prepare data in list format"""
            try:
                purchases_json = req.json()
                for purchase in purchases_json['rows']:
                    purchase_date_0 = datetime.strptime(str(purchase['moment']),'%Y-%m-%d %H:%M:%S.%f').date()
                    purchase_date = purchase_date_0.strftime("%d.%m.%y")
                    purchase_name = purchase['name']
                    purchase_in_name = purchase['incomingNumber']
                    purchase_in_date0 = datetime.strptime(str(purchase['incomingDate']), '%Y-%m-%d %H:%M:%S.%f').date()
                    purchase_in_date = purchase_in_date0.strftime("%d.%m.%y")
                    purchase_sum = purchase['sum']/100
                    if purchase['vatEnabled']: purchase_vat = purchase['vatSum']/100
                    else: purchase_vat = 0

                    try:
                        f_in_link = purchase['factureIn']['meta']['href']
                        facture_data = self.request_facturein_data(f_in_link)
                    except:
                        #continue
                        facture_data = [purchase_in_name, purchase_in_date, '0']

                    try:
                        customer_link = purchase['agent']['meta']['href']
                        customer_data = self.request_customer_data(customer_link)
                    except:
                        continue
                        customer_data = ['неизвестно', 'неизвестно']

                    position += 1
                    doc_sum += purchase_sum
                    vatsum += purchase_vat
                    data_linked.append([position, facture_data[1], facture_data[0],
                                        customer_data[0], customer_data[1], 'Российский рубль,643',
                                        purchase_sum, purchase_vat])
            except IndexError:
                print('Error, cant prepare array for sales book ', Exception)

        except IndexError:
            print('Error, cant get sales list from MS', Exception)

        #data_linked = sorted(data_linked, key=lambda y: (y[1], y[4], y[2]))  # sorting by group and name
        data_linked = self.purchase_arr + data_linked
        data_linked.append(['', '', '',
                            '', '', '',
                            doc_sum, vatsum])
        return data_linked

    def get_customers_list(self):
        """'''Return customer name'''"""
        try:
            req = requests.get(url=url_customers, headers=header_for_token_auth)
            with open('customers_list.json', 'w') as ff:
                json.dump(req.json(), ff, ensure_ascii=False)
            return req.json()['name']

        except IndexError:
            print('Sorry, cant get customers list ')
            return False

def fill_the_sales_book(start_day='2021-05-01', end_day='2021-05-31'):
    get_new_data_for_sales_book = moi_sklad()
    data_for_sales_book = get_new_data_for_sales_book.get_sales_list(start_day, end_day)
    new_sales_books = sp_books()
    new_sales_books.clear_data_sheet(1)
    new_sales_books.append_array(data_for_sales_book, 1)
    return work_book

def fill_the_purchases_book(start_day='2021-05-01', end_day='2021-05-31'):
    get_new_data_for_purchases_book = moi_sklad()
    data_for_purchases_book = get_new_data_for_purchases_book.get_purchases_list(start_day, end_day)
    new_sales_books = sp_books()
    new_sales_books.clear_data_sheet(0)
    new_sales_books.append_array(data_for_purchases_book, 0)
    return work_book

#fill_the_purchases_book()
#fill_the_sales_book()