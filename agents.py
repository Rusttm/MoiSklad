# -*- coding: utf8 -*-
"""this module is for sales and purchases books forms"""
import requests
import json
import configparser
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


try:
    conf = configparser.ConfigParser()
    conf.read('agents.ini')
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
    saratov_book = conf['GOOGLE']['saratov_book']
    nsk_book = conf['GOOGLE']['nsk_book']
    saratov_link = conf['GOOGLE']['saratov_link']
    nsk_link = conf['GOOGLE']['nsk_link']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE_MACOS']
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
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

class agents_books():
    """new class for sales and purchases books"""
    def __init__(self, work_book = saratov_book, start_day='2021-02-08', end_day='2021-02-28'):
        self.start_day = start_day
        self.end_day = end_day
        self.bookId = work_book
        self.bookName = 'Отчет агента'
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

class moi_sklad():
    def __init__(self, start_day='2021-02-08', end_day=toda_y_date):
        self.start_day = start_day
        self.end_day = end_day
        self.product_dict = {}
        self.demands_payed_dict = {}
        self.sales_arr=[['№ п/п', 'Дата отгрузки', 'Номер отгрзки',
                        'Наименование покупателя', 'Стоимость продажи', 'Себестоимость',
                         'Прибыль', 'Оплачено', 'Группа'],
                        ['1', '2', '3', '4', '5', '6', '7', '8', '9']]

    def get_payments_list(self, start_day='2021-02-08', end_day=toda_y_date):
        """Return dict { demand_link : linked_sum}"""
        try:
            url_filtered = str(
                f'{url_payments_list}?order=moment,name&filter=moment>={start_day} 00:00:00.000;moment<={end_day} 23:00:00.000')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            #with open('payments_list.json', 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)
            try:
                for payment in req.json()['rows']:
                    payment['name'] # number
                    payment['moment']  # date
                    payment['sum']  # payment sum
                    try:
                        x = payment['operations']
                    except:
                        continue
                    for demand in payment['operations']:
                        if demand['meta']['type'] == "demand":
                            demand_link = demand['meta']['href']
                            if demand_link not in self.demands_payed_dict.keys():
                                self.demands_payed_dict[demand_link] = demand['linkedSum']
                            else:
                                self.demands_payed_dict[demand_link] += demand['linkedSum']
            except IndexError:
                print('Sorry, cant unroll payments list ')
        except IndexError:
            print('Sorry, cant get payments list ')

        return self.demands_payed_dict

    def get_profit_by_product_list(self, start_day='2021-02-08', end_day=toda_y_date):
        """'''Return dict { prod_link : sale_cost}'''"""
        try:
            url_filtered = str(f'{url_profit_product}?momentFrom=2021-02-08 01:00:00')
                #f'{url_profit_product}?momentFrom={start_day} 00:00:00;momentTo={end_day} 23:00:00')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            with open('profit_prod_list.json', 'w') as ff:
                json.dump(req.json(), ff, ensure_ascii=False)
            for elem in req.json()['rows']:
                self.product_dict[elem['assortment']['meta']['href']] = elem['sellCost']/100
            return self.product_dict

        except IndexError:
            print('Sorry, cant get products dict ')
            return False

    def get_positions_costsum(self, positions_link='https://online.moysklad.ru/api/remap/1.2/entity/demand/5c1b5f34-69ce-11eb-0a80-05f4002445e1/positions'):
        """'''Return cost summ of positions in demand'''"""
        pos_cost_sum = 0
        try:
            req = requests.get(url=positions_link, headers=header_for_token_auth)
            #with open('profit_prod_list.json', 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)
            for position in req.json()['rows']:
                pos_link = position['assortment']['meta']['href']
                pos_cost = self.product_dict[pos_link]
                pos_qty = position['quantity']
                pos_cost_sum += pos_qty * pos_cost
        except IndexError:
            print('Sorry, cant get products dict ')
        return pos_cost_sum

    def request_customer_data(self, customer_link):
        """return data from facture """
        try:
            customer_req = requests.get(url=customer_link, headers=header_for_token_auth)
            customer = customer_req.json()
            group_request = requests.get(url=customer['group']['meta']['href'], headers=header_for_token_auth)
            customer_group = group_request.json()['name']
            customer_data_list = [customer['name'], customer_group]
            return customer_data_list
        except IndexError:
            print(f'Error, cant find the customer {customer_link}', Exception)

    def get_sales_list(self, agent_name = 'Саратов', start_day='2021-02-08', end_day=toda_y_date):
        """'''get sales list from MS and put it in file .json'''"""
        data_linked = []
        saratov_data_linked = []
        nsk_data_linked = []
        doc_sum = 0
        cost_sum = 0
        profit_sum = 0
        payed_sum = 0
        vatsum = 0
        position = 0
        try:
            product_profit = self.get_profit_by_product_list(start_day, end_day)
            payments = self.get_payments_list(start_day, end_day)
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
                    sale_payed_sum = sale['payedSum']/100
                    if sale['vatEnabled']: sale_vat = sale['vatSum']/100
                    else: sale_vat = 0
                    try:
                        customer_link = sale['agent']['meta']['href']
                        customer_data = self.request_customer_data(customer_link)
                    except:
                        continue

                    # skip non requested groups
                    if customer_data[1] != agent_name: continue

                    try:
                        payed = payments[sale['meta']['href']]/100
                    except:
                        payed = 0

                    positions_in_sale_link = sale['positions']['meta']['href']
                    sale_cost_sum = self.get_positions_costsum(positions_in_sale_link)
                    position += 1
                    doc_sum += sale_sum
                    vatsum += sale_vat
                    cost_sum += sale_cost_sum
                    profit_sum = doc_sum - sale_cost_sum
                    payed_sum += payed
                    data_linked.append([position, sale_date, sale_name,
                                        customer_data[0], sale_sum, sale_cost_sum,
                                        sale_sum-sale_cost_sum, sale_payed_sum, customer_data[1]])

            except IndexError:
                print('Error, cant prepare array for sales book ', Exception)

        except IndexError:
            print('Error, cant get sales list from MS', Exception)

        #data_linked = sorted(data_linked, key=lambda y: (y[1], y[4], y[2]))  # sorting by group and name
        data_linked = self.sales_arr + data_linked
        data_linked.append(['', '', '', '',
                            doc_sum, cost_sum, profit_sum,
                            payed_sum, ''])
        return data_linked




def get_pfo_agent_report():
    """на четверг сделать выборку по оплатам вывести все оплаченные отгрузки
    занести платежи в 1С и проверить по тем отгрузкам, есть ли неоплачеенные?
    надо найти почти 200к отгрузок
    """
    pfo_report = moi_sklad()
    pfo_report_book = agents_books(saratov_book)
    pfo_report_book.clear_data_sheet()
    pfo_report_book.append_array(pfo_report.get_sales_list())
    #print(pfo_report.get_profit_by_product_list())
    #print(pfo_report.get_positions_costsum('https://online.moysklad.ru/api/remap/1.2/entity/demand/5c1b5f34-69ce-11eb-0a80-05f4002445e1/positions'))

get_pfo_agent_report()

