# -*- coding: utf8 -*-
"""this module is for sales and purchases books forms"""
import requests
import json
import configparser
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import xlsxwriter


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
    temp_book = conf['GOOGLE']['temp_book']
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
    def __init__(self, agent_name = "Саратов"):
        self.bookName = 'Отчет агента'
        self.email = 'rustammazhatov@gmail.com'
        self.sheets = []
        self.sheets_dict = {}
        self.today_date = str(datetime.now().strftime("%Y%m%d"))
        if agent_name == "Саратов": self.bookId = saratov_book
        elif agent_name == "Новосибирск": self.bookId = nsk_book
        else:
            print('Data was send to Temporary book')
            self.bookId = temp_book

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
    def __init__(self, agent_name = 'Саратов', start_day='2021-02-08', end_day=toda_y_date):

        self.agent_name = agent_name
        self.start_day = start_day
        self.end_day = end_day
        self.payed_demand_data_linked = []
        self.product_dict = {}
        self.demands_payed_dict = {}
        self.skipped_customers_name = ['ООО "ТРЕЙД-НСК"', 'ИП Горбунов Алексей Анатольевич', 'биэс ч\л',
                                       'ЭРА ч.л.', 'Ульяновск ч\л']
        self.sales_arr=[['№ п/п', 'Дата отгрузки', 'Номер отгрузки',
                        'Наименование покупателя', 'Стоимость продажи', 'Себестоимость',
                         'Прибыль', 'Оплачено', 'Группа'],
                        ['1', '2', '3', '4', '5', '6', '7', '8', '9']]

    def get_payments_list(self):
        """Return dict { demand_link : linked_sum}"""
        start_day =  self.start_day
        end_day = self.end_day
        try:
            url_filtered = str(
                f'{url_payments_list}?order=moment,name&filter=moment>={start_day} 00:00:00.000;moment<={end_day} 23:00:00.000')
            req = requests.get(url=url_filtered, headers=header_for_token_auth)
            #with open('payments_list.json', 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)
            try:
                for payment in req.json()['rows']:
                    #payment['name'] # number
                    #payment['moment']  # date
                    #payment['sum']  # payment sum
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

    def get_profit_by_product_list(self):
        """'''Return dict { prod_link : sale_cost}'''"""
        #start_day = self.start_day
        start_day_for_sales =  self.start_day
        end_day = self.end_day
        try:
            url_filtered = str(f'{url_profit_product}?momentFrom={start_day_for_sales} 00:00:00') # !momentTo doesnt work
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

    def get_positions_costsum(self, positions_link):
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

    def get_info_from_demand(self, demand_link):
        """Return array [customer_name, demandNo, demandDate, demandSum, demandPayedSum, customerGroup]"""
        try:
            demand_req_json = requests.get(url=demand_link, headers=header_for_token_auth)
            #with open('demand_structure.json', 'w') as ff:
            #    json.dump(req.json(), ff, ensure_ascii=False)
            demand_req = demand_req_json.json()
            customer_link = demand_req['agent']['meta']['href']
            customer_req = self.request_customer_data(customer_link)
            customer_name = customer_req[0]
            customer_group = customer_req[1]
            demand_no = demand_req['name']
            demand_date = demand_req['moment']
            demand_sum = demand_req['sum']
            demand_payed_sum = demand_req['payedSum']
            return [customer_name, demand_no, demand_date, demand_sum, demand_payed_sum, customer_group]
        except IndexError:
            print('Sorry, cant get products dict ')
            return ['NA','NA','NA',0,0]

    def get_sales_list(self):
        """'''get sales list from MS and put it in file .json'''"""
        start_day = self.start_day
        end_day = self.end_day
        agent_name = self.agent_name
        data_linked = []
        doc_sum = 0
        cost_sum = 0
        profit_sum = 0
        payed_sum = 0
        vatsum = 0
        position = 0
        payed_sum2 = 0
        try:
            product_profit = self.get_profit_by_product_list()
            payments = self.get_payments_list()
            start_day_for_sales = start_day
            url_filtered = str(
                f'{url_otgruzka_list}?order=moment,name&filter=moment>={start_day_for_sales} 00:00:00.000;moment<={end_day} 23:00:00.000')
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

                    # skip agents
                    if customer_data[0] in self.skipped_customers_name:
                        continue

                    # skip non requested groups
                    if customer_data[1] != agent_name:
                        continue



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
                    profit_sum += sale_sum - sale_cost_sum
                    payed_sum += payed  #sum for payment in requested period
                    payed_sum2 += sale_payed_sum  # payments for demand
                    data_linked.append([position, sale_date, sale_name,
                                        customer_data[0], sale_sum, sale_cost_sum,
                                        (sale_sum - sale_cost_sum), sale_payed_sum, customer_data[1]])

            except IndexError:
                print('Error, cant prepare array for sales book ', Exception)

        except IndexError:
            print('Error, cant get sales list from MS', Exception)

        #data_linked = sorted(data_linked, key=lambda y: (y[1], y[4], y[2]))  # sorting by group and name
        data_linked = self.sales_arr + data_linked
        data_linked.append(['', '', '', '',
                            doc_sum, cost_sum, profit_sum,
                            payed_sum2, payed_sum])
        data_linked += self.get_1c_sales_list() 
        return data_linked

    def get_1c_sales_list(self):
        """'''get sales list from MS and put it in file .json'''"""
        start_day = self.start_day
        end_day = self.end_day
        agent_name = self.agent_name
        self.payed_demand_data_linked = []
        doc_sum = 0
        cost_sum = 0
        profit_sum = 0
        payed_sum = 0
        vatsum = 0
        position = 0
        try:
            payments = self.demands_payed_dict
            for payment, payment_sum in payments.items():
                demand_info = self.get_info_from_demand(payment)
                if demand_info[5] != agent_name: continue
                demand_date_temp = demand_info[2]
                demand_date = datetime.strptime(demand_date_temp,'%Y-%m-%d %H:%M:%S.%f')
                req_date = datetime.strptime(self.start_day,'%Y-%m-%d')
                # filtered date before requested
                if demand_date < req_date:
                    position += 1
                    self.payed_demand_data_linked.append(
                        [position, str(demand_date.strftime("%d.%m.%Y")),
                         demand_info[1], demand_info[0], demand_info[3]/100,
                         '','',demand_info[4]/100, demand_info[5]]
                    )
                else: continue
        except IndexError:
            print('Error, cant prepare array for sales book ', Exception)
        #data_linked = sorted(data_linked, key=lambda y: (y[1], y[4], y[2]))  # sorting by group and name
        return self.payed_demand_data_linked



def get_pfo_agent_report():
    """на четверг сделать выборку по оплатам вывести все оплаченные отгрузки
    занести платежи в 1С и проверить по тем отгрузкам, есть ли неоплачеенные?
    надо найти почти 200к отгрузок
    """
    pfo_report = moi_sklad(agent_name = 'Саратов', start_day='2021-03-01', end_day='2021-03-31')
    pfo_report_book = agents_books(agent_name = "Саратов")

    pfo_report_book.clear_data_sheet()
    req_list = pfo_report.get_sales_list()
    workbook = xlsxwriter.Workbook('pfo_report.xlsx')
    worksheet = workbook.add_worksheet('temporary1')
    col = 0
    for row, data in enumerate(req_list):
        worksheet.write_row(row, col, data)
    workbook.close()
    pfo_report_book.append_array(req_list)
    #print(pfo_report.get_profit_by_product_list())
    #print(pfo_report.get_positions_costsum('https://online.moysklad.ru/api/remap/1.2/entity/demand/5c1b5f34-69ce-11eb-0a80-05f4002445e1/positions'))


def get_nsk_agent_report():
    """на четверг сделать выборку по оплатам вывести все оплаченные отгрузки
    занести платежи в 1С и проверить по тем отгрузкам, есть ли неоплачеенные?
    надо найти почти 200к отгрузок
    """
    nsk_report = moi_sklad(agent_name = 'Новосибирск', start_day='2021-02-08', end_day='2021-03-30')
    nsk_report_book = agents_books(agent_name = "Новосибирск")

    nsk_report_book.clear_data_sheet()
    nsk_req_list = nsk_report.get_sales_list()
    workbook = xlsxwriter.Workbook('nsk_report.xlsx')
    wsh_name = 'Март'
    worksheet = workbook.add_worksheet(wsh_name)
    col = 0
    for row, data in enumerate(nsk_req_list):
        worksheet.write_row(row, col, data)
    workbook.close()
    nsk_report_book.append_array(nsk_req_list)


get_pfo_agent_report()