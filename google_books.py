import configparser
import httplib2
import googleapiclient.discovery
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path
import gspread
from gspread_dataframe import set_with_dataframe
import locale
import os

#locale.setlocale(locale.LC_ALL, 'fr_FR')
#locale.setlocale(locale.LC_ALL, 'ru_RU')

try:
    conf = configparser.ConfigParser()
    #conf.read('/Volumes/GoogleDrive/My Drive/Python/MoiSklad/MoiSklad/google_books.ini') # macos version
    #conf.read('./google_books.ini') # WINdows version path
    conf.read(os.path.join(os.path.dirname(__file__), 'config/google_books.ini'))
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
    CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILE)
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

    #  sheetList = spreadsheet.get('sheets')
    #  sheetName = sheetList[0]['properties']['title']  # '2021y'
except IndexError:
    print('Cant read account data', Exception)


def ini_file_write(file_name='google_sheet.ini',
                   tree='NEW_BOOKS', section='unknown', entry='unknown'):
    try:
        ini_file = Path(file_name)
        config = configparser.ConfigParser()
        config.read(ini_file)
        config.set(tree, section, entry)
        config.write(ini_file.open("w"))
    except IndexError:
        print('ini file hasnt updated', Exception)

toda_y1 = str(datetime.now().strftime("%Y%m%d"))

class GoogleBook:
    def __init__(self, work_spreadsheetid = test_spreadsheetId):
        self.bookId = work_spreadsheetid
        self.bookName = 'Testing google sheets'
        self.email = 'rustammazhatov@gmail.com'
        self.sheets = []
        self.new_sheet =  toda_y1

    def make_book(self):
        """make a new book and Return book id"""
        try:
            toda_y = str(datetime.now().strftime("%Y%m%d"))
            new_spreadsheet = service.spreadsheets().create(body={
                'properties': {'title': self.bookName, 'locale': 'en_US'},
                'sheets': [{'properties': {'sheetType': 'GRID',
                                           'sheetId': 0,
                                           'title': toda_y,
                                           'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
            }).execute()
            new_spreadsheetid = new_spreadsheet['spreadsheetId']  # сохраняем идентификатор файла
            book_link = str('https://docs.google.com/spreadsheets/d/' + new_spreadsheetid)
            ini_file_write(section=book_link)
            self.give_access_to_book()
            return new_spreadsheetid
        except IndexError:
            print('Cant make the book', Exception)

    def give_access_to_book(self, user_mail = 'rustammazhatov@gmail.com'):
        try:
            # Выбираем работу с Google Drive и 3 версию API
            drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
            access = drive_service.permissions().create(
                fileId = self.bookId,
                body = {'type': 'user', 'role': 'writer', 'emailAddress': user_mail},
                # Открываем доступ на редактирование
                fields = 'id').execute()
            ini_file_write(section='access_id', entry=access['id'])
            return True
        except IndexError:
            print(f'Cant create accsess for {self.email} to the book', Exception)
            return False

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

    def make_new_sheet(self, new_sheet_name = toda_y1):
        try:
            got_list = self.get_sheets_list()
            got_list = sorted(got_list, key=lambda y: (y[0], y[1]))
            last_id = got_list[-1][0]+1  # find last id
            got_sheet_names = [x[1] for x in got_list]  #make list of sheets
            shift = 0
            while new_sheet_name in got_sheet_names:
                new_sheet_name = f"{new_sheet_name}_{shift}"
                shift+= 1
            request_body={
                "requests": [{
                    "addSheet": {
                    "properties":{
                        "sheetId": last_id,
                        "title": new_sheet_name,
                        "tabColor": {
                        "red": 0.01,
                        "green": 0.9,
                        "blue" : 0.9
                        }
                    }
                 }
            }]}
            new_sheet_req = service.spreadsheets().batchUpdate(
                spreadsheetId = self.bookId,
                body = request_body).execute()
            return new_sheet_req
        except IndexError:
            print('Cant make new sheet in the book', Exception)
            return Exception

    def clear_data_sheet(self, sheetid = 0, clear_range='A1:M1000'):
        try:
            worksheet = gc.open_by_key(self.bookId).get_worksheet(sheetid)  # sheetID = 0
            range_of_cells = worksheet.range(clear_range)  # -> Select the range you want to clear
            for cell in range_of_cells:
                cell.value = ''
            worksheet.update_cells(range_of_cells)
            return True
        except IndexError:
            print(f'Cant clear {sheetid} sheet', Exception)
            return Exception

    def append_df(self, work_df, sheetid = 0):
        try:
            worksheet = gc.open_by_key(self.bookId).get_worksheet(sheetid)  # sheetID = 0
            set_with_dataframe(worksheet, work_df)
            return True
        except IndexError:
            print('Cant make new sheet in the book', Exception)
            return Exception

    def append_array(self, work_array, sheetid=0):
        try:
            values =  {'values' : work_array}
            result = service.spreadsheets().values().append(
                spreadsheetId=self.bookId, range='A1:P1000',
                valueInputOption='RAW',
                body=values).execute()
            return result
        except IndexError:
            print('Cant make new sheet in the book', Exception)
            return Exception

    def append_forest(self, name_array = [], price_array = []):
        zipped_data = []
        if len(name_array) == len(price_array):
            for i in range(len(name_array)):
                zipped_data.append([name_array, price_array])
        print(zipped_data)
        try:
            values =  {'values' : zipped_data}
            result = service.spreadsheets().values().append(
                spreadsheetId=self.bookId,
                range='A1:P1000',
                valueInputOption='RAW',
                body=values).execute()
            return result
        except IndexError:
            print('Cant append data to sheet in the book', Exception)
            return Exception

def send_to_forest_sheet(name_array =[], price_array=[]):
    zipped_data = []
    if len(name_array) == len(price_array):
        for i in range(len(name_array)):
            zipped_data.append([name_array[i], locale.atof(price_array[i])])
    work_forest_book = GoogleBook(parsing_book)
    #work_forest_book.clear_data_sheet()
    work_forest_book.append_array(zipped_data)
    return zipped_data

def fill_the_debt_gb(columns_for_df = [],data_linked = []):
    """make files within debt"""
    try:
        data_linked = sorted(data_linked, key=lambda y: (y[1], y[2], y[3]))  # sorting by group and name
        nsk_debt = [elem for elem in data_linked if elem[1] == 'новосибирскконтрагенты']
        pfo_debt = [elem for elem in data_linked if elem[1] == 'покупатели пфо']


        debt_gb = GoogleBook(debt_book)
        debt_gb.clear_data_sheet()
        debt_gb.append_array([columns_for_df])
        debt_gb.append_array(data_linked)

        debt_nsk_gb = GoogleBook(debt_nsk)
        debt_nsk_gb.clear_data_sheet()
        debt_nsk_gb.append_array([columns_for_df])
        debt_nsk_gb.append_array(nsk_debt)

        debt_pfo_gb = GoogleBook(debt_pfo)
        debt_pfo_gb.clear_data_sheet()
        debt_pfo_gb.append_array([columns_for_df])
        debt_pfo_gb.append_array(pfo_debt)
        return 'GoogleTables filled'

    except IndexError:
        print('Cant append data to debt book', Exception)
        return 'GoogleTables NOT renewed'

#fill_the_debt_gb(columns_for_df, data_linked)

#forest_pars=GoogleBook(parsing_book)
#forest_pars.make_new_sheet()