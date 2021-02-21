import configparser
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path
from pprint import pprint
import googleapiclient
from googleapiclient import discovery
from google.cloud import storage
#from google import Create_Service
import google

# pip install --upgrade google-cloud-storage



try:
    conf = configparser.ConfigParser()
    conf.read('google_sheet.ini')
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']  # Имя файла с закрытым ключом, вы должны подставить свое
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheetId = conf['GOOGLE']['spreadsheetId']
    test_spreadsheetId = conf['GOOGLE']['test_spreadsheetId']
    serman_book = conf['GOOGLE']['serman_book']
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build(API_SERVICE_NAME, API_VERSION, http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
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
            last_id = got_list[-1][0]+1
            request_body={
                "requests": [{
                    "addSheet": {
                    "properties":{
                        "sheetId": last_id,
                        #"title": new_sheet_name,
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


work_serman_book=GoogleBook(serman_book)
#new_book=GoogleBook(x)
print(work_serman_book.make_new_sheet())
#print(work_serman_book.get_sheets_list())

