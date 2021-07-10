import configparser
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from datetime import datetime
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR')

try:
    conf = configparser.ConfigParser()
    conf.read(os.path.join(os.path.dirname(__file__), 'config/google_books.ini'))
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
    CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), f'config/{CREDENTIALS_FILE}')
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheetId = conf['GOOGLE']['spreadsheetId']
    test_spreadsheetId = conf['GOOGLE']['test_spreadsheetId']
    serman_book = conf['GOOGLE']['serman_book']
    parsing_book = conf['GOOGLE']['parsing_book']
    parsing_forest_sheet_id = conf['GOOGLE']['parsing_forest_sheet_id']
    debt_book = conf['GOOGLE']['debt_book']
    debt_nsk = conf['GOOGLE']['debt_nsk']
    debt_pfo = conf['GOOGLE']['debt_pfo']
        # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build(API_SERVICE_NAME, API_VERSION, http=httpAuth, cache_discovery=False)  # Выбираем работу с таблицами и 4 версию API
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    gc = gspread.service_account(filename=CREDENTIALS_FILE)

except IndexError:
    print('Cant read account data', Exception)


class GoogleBook:

    def __init__(self, work_book=parsing_book):
        self.bookId = work_book
        self.bookName = 'Testing google sheets'
        self.email = 'rustammazhatov@gmail.com'
        self.sheets = {}
        self.full_path = 'NONE'
        self.new_sheet = str(datetime.now().strftime("%Y%m%d"))
        self.get_sheets_list()


    def get_sheets_list(self):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=self.bookId).execute()
            sheetList = spreadsheet.get(API_SERVICE_NAME)
            for sheet in sheetList:
                sheet_id_number = sheet['properties']['sheetId']
                sheet_name = sheet['properties']['title']
                self.sheets[str(sheet_id_number)] = sheet_name
                self.sheets[sheet_name] = str(sheet_id_number)
            return self.sheets
        except IndexError:
            print(f'Cant get sheet list of the book', Exception)
            return {'0': 'NoName', 'NoName': '0'}

    def clear_list(self):
        try:
            worksheet = gc.open_by_key(self.bookId).get_worksheet(self.sheetId)  # sheetID = 0
            sheetName = self.sheets[str(self.sheetId)]
            rangeAll = '{0}!A1:D1000'.format(sheetName)
            body = {}
            resultClear = service.spreadsheets().values().clear(spreadsheetId=self.bookId, range=rangeAll,
                                                                body=body).execute()
            print(resultClear)
            #other methon for clear sheet
            # range_of_cells = worksheet.range(rangeAll)  # -> Select the range you want to clear
            # for cell in range_of_cells:
            #     cell.value = ''
            # worksheet.update_cells(range_of_cells)
            return True
        except IndexError:
            print(f'Cant clear {self.sheetId} sheet', Exception)
            return Exception

    def append_array(self, work_array, sheetId='1238490361'):
        self.sheetId = int(sheetId)
        self.clear_list()
        try:
            sheetName = self.sheets[sheetId]
            rangeAll = '{0}!A1:D1000'.format(sheetName)
            values =  {'values' : work_array}
            result = service.spreadsheets().values().append(
                spreadsheetId=self.bookId,
                range=rangeAll,
                valueInputOption='RAW',
                body=values).execute()
            self.full_path = f'https://docs.google.com/spreadsheets/d/{self.bookId}/edit#gid={self.sheetId}'
            return self.full_path
        except IndexError:
            print('Cant fill sheet in the book', Exception)
            return self.full_path


# work_array = [(1,1)]
# x = GoogleBook(work_book='1_C6uxRFz5wb8K_Cu4c4HcUn8EYk0vnhARhA_UvtKT1c')
# x.append_array(work_array=work_array, sheetId='1238490361')
# print(x.get_sheets_list())