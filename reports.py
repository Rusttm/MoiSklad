"""управленческие отчеты"""
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
    # goggle parts
    report_book = conf['GOOGLE']['report_book']
    profit_book = conf['GOOGLE']['profit_book']
    temp_book = conf['GOOGLE']['temp_book']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    print(f'Googgle book https://docs.google.com/spreadsheets/d/{report_book}/edit#gid=0 initiated')
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



class report_book():
    def __init__(self):
        self.bookName = 'Отчеты управленческие'
        self.email = 'rustammazhatov@gmail.com'
        self.bookId = profit_book
        self.today_date = str(datetime.now().strftime("%Y%m%d"))
        self.sheets = []

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


new_report = report_book()
new_report.give_access_to_book()
print(new_report.get_sheets_list(profit_book))
