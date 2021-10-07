# module for work with Google books
import configparser
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from datetime import datetime




class ServiceGoogleBook():
    def __init__(self, work_book):
        self.conf = configparser.ConfigParser()
        self.conf.read(os.path.join(os.path.dirname(__file__), 'config/google_books.ini'))
        try:
            self.bookId = self.conf['GOOGLE'][work_book]
            #print(f'{work_book} is initialized')
        except Exception as m:
            print(f'cant find {work_book} GoogleBook', m)
        self.sheetId = 0
        self.sheets = {}  #dictionary of sheets in book {sheetID:sheetName}
        self.gb_starts()
        self.get_sheets_list()

    def gb_starts(self):
        try:
            CREDENTIALS_FILE = self.conf['GOOGLE']['CREDENTIALS_FILE']
            CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), f'config/{CREDENTIALS_FILE}')
            API_SERVICE_NAME = 'sheets'
            API_VERSION = 'v4'
            req = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, req)
            httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
            self.service = apiclient.discovery.build(API_SERVICE_NAME, API_VERSION, http=httpAuth, cache_discovery=False)  # Выбираем работу с таблицами и 4 версию API
            #print(f'Goggle Books is initialized')
        except Exception as m:
            print('Goggle Books is not initialized:', m)

    def get_sheets_list(self):
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.bookId).execute()
            sheetList = spreadsheet.get('sheets')
            for sheet in sheetList:
                sheet_id_number = sheet['properties']['sheetId']
                sheet_name = sheet['properties']['title']
                self.sheets[str(sheet_id_number)] = sheet_name
                self.sheets[sheet_name] = str(sheet_id_number)
            return self.sheets

        except IndexError:
            print(f'Cant get sheet list of the book', Exception)
            return {'0': 'NoName', 'NoName': '0'}

    def clear_list(self, sheetID = 0):
        try:
            self.sheetId = sheetID
            sheetName = self.sheets[str(self.sheetId)]
            rangeAll = '{0}!A1:Z1000'.format(sheetName)
            body = {}
            self.service.spreadsheets().values().clear(spreadsheetId=self.bookId, range=rangeAll, body=body).execute()
            return True
        except Exception as m:
            print(f'Cant clear {self.sheetId} sheet', m)
            return False

    def append_string(self, work_array, sheetId=0):
        self.sheetId = int(sheetId)
        try:
            sheetName = self.sheets[str(self.sheetId)]
            rangeAll = '{0}!A1:H1000'.format(sheetName)
            values =  {'values' : work_array}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.bookId,
                range=rangeAll,
                valueInputOption='RAW',
                body=values).execute()
            self.full_path = f'https://docs.google.com/spreadsheets/d/{self.bookId}/edit#gid={self.sheetId}'
            return self.full_path
        except Exception as m:
            print('Cant fill sheet in the book', m)
            return self.full_path
        print('data to GoogleBook was wrote')


# book = ServiceGoogleBook(work_book='balance_book')
# x=[[1,2,3,4,5]]
# req = book.append_string(work_array=x, sheetId=0)
# print(req)