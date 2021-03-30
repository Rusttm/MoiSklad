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

#locale.setlocale(locale.LC_ALL, 'fr_FR')
locale.setlocale(locale.LC_ALL, 'ru_RU')

try:
    conf = configparser.ConfigParser()
    #conf.read('/Volumes/GoogleDrive/My Drive/Python/MoiSklad/MoiSklad/google_books.ini') # macos version
    conf.read('D:/Python_proj/MoiSklad/google_books.ini') # WINdows version path
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE_WINOS']
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

data_linked=[['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 99 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=02631baa-6613-11eb-0a80-006c000ba223', 21, 7, 6610.94, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 71 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=0c84092f-6548-11eb-0a80-095b000a745f', 30, 9, 120621.42, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'ЭРА ч.л.', '№ 83 от 2021-01-28', 'https://online.moysklad.ru/app/#demand/edit?id=0d377794-66bd-11eb-0a80-018700056801', 0, -20, 17425.8, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 144 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=1336812d-7022-11eb-0a80-032000048430', 14, 13, 99125.76, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 351 от 2020-08-11', 'https://online.moysklad.ru/app/#demand/edit?id=1e832980-6533-11eb-0a80-046b00063f53', 0, -190, 28800.8, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 132 от 2021-02-12', 'https://online.moysklad.ru/app/#demand/edit?id=21493dec-6ce3-11eb-0a80-036100021a68', 21, 16, 5851.2, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 139 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=231f845c-7006-11eb-0a80-04e50002a652', 14, 13, 6475.0, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 72 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=29dfb18d-6548-11eb-0a80-03c0000a6d71', 30, 9, 571825.18, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 101 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=399be511-6613-11eb-0a80-06c5000bae7e', 14, 0, 27600.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 318 от 2020-07-29', 'https://online.moysklad.ru/app/#demand/edit?id=3bf93452-6532-11eb-0a80-03c00005e1bd', 0, -203, 24193.11, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 125 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=3c5469f7-6c4c-11eb-0a80-047c001a8498', 14, 8, 14000.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 116 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=3ed8a706-6abe-11eb-0a80-0067000a5ab6', 0, -8, 25411.5, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 74 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=3ef4d612-6549-11eb-0a80-02fb000a5f76', 21, 0, 145.5, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'ООО "ТРЕЙД-НСК"', '№ 86 от 2021-01-29', 'https://online.moysklad.ru/app/#demand/edit?id=45edbd61-654b-11eb-0a80-07f1000aa0ff', 30, 11, 12746.5, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 115 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=465ca1ed-6aa5-11eb-0a80-06da00056fc3', 0, -8, 23735.57, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 141 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=46e82a2d-701b-11eb-0a80-060800038de1', 21, 20, 246.68, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 360 от 2020-08-14', 'https://online.moysklad.ru/app/#demand/edit?id=49625a11-6533-11eb-0a80-03c000061465', 0, -187, 21976.34, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТАТСТРОЙКАМА"', '№ 710 от 2020-12-17', 'https://online.moysklad.ru/app/#demand/edit?id=51fcaba7-6530-11eb-0a80-016900053e5b', 14, -48, 6727.33, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 109 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=52804313-6a87-11eb-0a80-02d9000299be', 14, 6, 15688.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБКЕДР"', '№ 124 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=56ab95c0-6c38-11eb-0a80-086b0016a127', 14, 8, 14069.66, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 102 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=5816fa8b-6654-11eb-0a80-021500016fe0', 30, 16, 22750.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 147 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=58be0543-70e0-11eb-0a80-024500014e24', 0, 0, 3961.67, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 8 от 2021-01-12', 'https://online.moysklad.ru/app/#demand/edit?id=5a320f8f-6534-11eb-0a80-046b0006833e', 14, -22, 41944.16, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 127 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=5cd75d2d-6c59-11eb-0a80-050f001cdf2e', 0, -6, 41817.0, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 133 от 2021-02-12', 'https://online.moysklad.ru/app/#demand/edit?id=5d0ef4a0-6ce8-11eb-0a80-0495000332b0', 21, 16, 992.31, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "АВРО"', '№ 358 от 2020-08-13', 'https://online.moysklad.ru/app/#demand/edit?id=64dc4edf-6515-11eb-0a80-03c0000176e4', 21, -167, 1463.98, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 87 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=68381e78-654b-11eb-0a80-03c0000b0582', 21, 5, 38160.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ЕВРОПЛАСТ-Ф"', '№ 148 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=6afd74a9-70ee-11eb-0a80-09050002d316', 21, 21, 110840.93, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 103 от 2021-02-04', 'https://online.moysklad.ru/app/#demand/edit?id=6b90cd1d-66f5-11eb-0a80-05e9000ffbb9', 14, 1, 4800.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'Ульяновск ч\\л', '№ 62 от 2021-01-25', 'https://online.moysklad.ru/app/#demand/edit?id=6d94ab5e-66bd-11eb-0a80-06cc0005e71a', 0, -23, 260896.1, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБИРСКИЙ ЛЕС"', '№ 341 от 2020-08-06', 'https://online.moysklad.ru/app/#demand/edit?id=7338e1a3-652e-11eb-0a80-07f10004e407', 14, -181, 13873.03, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 136 от 2021-02-15', 'https://online.moysklad.ru/app/#demand/edit?id=77bed696-6f49-11eb-0a80-03610023352f', 0, -2, 2549.52, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ООО "БМ ГРУПП"', '№ 126 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=780be9b7-6c4f-11eb-0a80-034b001afca3', 0, -6, 65600.52, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 76 от 2021-01-28', 'https://online.moysklad.ru/app/#demand/edit?id=806b10a3-6549-11eb-0a80-0169000a3bf9', 21, 1, 1173.83, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 142 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=85628279-7021-11eb-0a80-09fb0004383c', 14, 13, 15688.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО ПКФ "МЕБЕЛЬНАЯ ФАБРИКА"', '№ 93 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=85f88009-6610-11eb-0a80-06c5000b13c2', 14, 0, 68720.76, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 377 от 2020-08-21', 'https://online.moysklad.ru/app/#demand/edit?id=87a0e491-6533-11eb-0a80-03c000061f86', 0, -180, 41003.32, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 69 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=88a66bc6-6548-11eb-0a80-07f10009fac4', 30, 9, 231224.97, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 48 от 2021-01-20', 'https://online.moysklad.ru/app/#demand/edit?id=893dcf75-6544-11eb-0a80-046b0009dd26', 30, 2, 46072.8, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 88 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=8fcd4294-654b-11eb-0a80-046b000b2df2', 21, 5, 14160.77, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТАРСК-НСК"', '№ 725 от 2020-12-23', 'https://online.moysklad.ru/app/#demand/edit?id=944aafbc-652f-11eb-0a80-095b00051ee3', 14, -42, 0.13000000000010914, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 118 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=96c68e3b-6ad3-11eb-0a80-0972000ed28a', 30, 22, 4823.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Михеева Нина Владимировна', '№ 128 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=99fe9b80-6c59-11eb-0a80-006c001dbe09', 0, -6, 164513.3, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ДМЭЛ"', '№ 146 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=9e07f5c4-70c5-11eb-0a80-0098000082be', 7, 7, 22624.45, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'Балаян Артик Арамович', '№ 128 от 2020-03-18', 'https://online.moysklad.ru/app/#demand/edit?id=9e497913-6522-11eb-0a80-03c00002f2a4', 0, -336, 0.010000000009313226, 'Просрочено!'], ['17.02.21', 'покупатели', 'ООО "ТРЕЙД-НСК"', '№ 723 от 2020-12-23', 'https://online.moysklad.ru/app/#demand/edit?id=a0a140af-6645-11eb-0a80-09660000a1d7', 30, -26, 33141.94, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 59 от 2021-01-22', 'https://online.moysklad.ru/app/#demand/edit?id=a2a9807d-6546-11eb-0a80-07f10009a1f7', 30, 4, 82600.56, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 89 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=a567f0b5-654b-11eb-0a80-02fb000ac985', 30, 14, 114769.17, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 49 от 2021-01-20', 'https://online.moysklad.ru/app/#demand/edit?id=aff86963-6544-11eb-0a80-046b0009e350', 21, -7, 2162.09, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБИРСКИЙ ЛЕС"', '№ 342 от 2020-08-06', 'https://online.moysklad.ru/app/#demand/edit?id=b2e18c43-652e-11eb-0a80-07f10004f00c', 14, -181, 4514.389999999999, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 60 от 2021-01-22', 'https://online.moysklad.ru/app/#demand/edit?id=b9269136-6546-11eb-0a80-06bd000a98e2', 30, 4, 11375.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 10 от 2021-01-12', 'https://online.moysklad.ru/app/#demand/edit?id=bc2cd42e-653c-11eb-0a80-01690007bce2', 14, -22, 1174.62, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "КРАСЛЕНТА"', '№ 31 от 2021-01-15', 'https://online.moysklad.ru/app/#demand/edit?id=bc8b68bc-653f-11eb-0a80-02fb00089407', 14, -19, 0.3999999999996362, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 143 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=c056a4c0-7021-11eb-0a80-052c00043846', 14, 13, 1716.66, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 395 от 2020-08-28', 'https://online.moysklad.ru/app/#demand/edit?id=c3ee4d16-6533-11eb-0a80-046b00065f0d', 0, -173, 45532.89, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ПАЛЛЕТ СЕРВИС"', '№ 117 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=c79ea5c6-6acc-11eb-0a80-0865000d2da2', 14, 6, 10471.939999999999, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 41 от 2021-01-19', 'https://online.moysklad.ru/app/#demand/edit?id=d6e3c2e6-6542-11eb-0a80-01690008dbe8', 14, -15, 12000.0, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ИП Добровольская Жанна Александровна', '№ 145 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=dc0150dc-7058-11eb-0a80-0320000eccdb', 0, -1, 328482.52, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 70 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=e08b22d5-6547-11eb-0a80-07f10009d6f1', 30, 9, 147009.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 121 от 2021-02-10', 'https://online.moysklad.ru/app/#demand/edit?id=e0dd1895-6b73-11eb-0a80-050f00056c8b', 21, 14, 301121.73, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ЕВРОПЛАСТ-Ф"', '№ 719 от 2020-12-22', 'https://online.moysklad.ru/app/#demand/edit?id=ec43307d-6527-11eb-0a80-095b0003a69c', 21, -36, 71293.92, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 24 от 2021-01-14', 'https://online.moysklad.ru/app/#demand/edit?id=ecbfbf4c-653e-11eb-0a80-095b0008ad8b', 14, -20, 5500.0, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 746 от 2020-12-28', 'https://online.moysklad.ru/app/#demand/edit?id=f13b06f5-6531-11eb-0a80-006700059dcf', 21, -30, 62737.16, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 407 от 2020-09-02', 'https://online.moysklad.ru/app/#demand/edit?id=f9b1c658-6533-11eb-0a80-06bd00064569', 0, -168, 76876.5, 'Просрочено!']]
scrapy_data =[['Скоба обивочная А-04cnk (80/04)', 'Скоба обивочная А-04cnk (80/04)', 'Скоба обивочная А-06 cnk (80/06)', 'Скоба обивочная А-06 cnk (80/06)', 'Скоба обивочная А-08 cnk (80/08)', 'Скоба обивочная А-08 cnk (80/08)', 'Скоба обивочная А-10 cnk (80/10)', 'Скоба обивочная А-10 cnk (80/10)', 'Скоба обивочная А-12 cnk (80/12)', 'Скоба обивочная А-12 cnk (80/12)', 'Скоба обивочная А-14 cnk (80/14)', 'Скоба обивочная А-14 cnk (80/14)', 'Скоба обивочная А-16 cnk (80/16)', 'Скоба обивочная А-16 cnk (80/16)', 'Скоба обивочная А-06 CRF', 'Скоба обивочная А-06 CRF', 'Скоба обивочная А-08 CRF', 'Скоба обивочная А-08 CRF', 'Скоба обивочная А-10 CRF', 'Скоба обивочная А-10 CRF', 'Скоба обивочная PF-06 CNK', 'Скоба обивочная PF-06 CNK', 'Скоба обивочная PF-09 CNK', 'Скоба обивочная PF-09 CNK', 'Скоба обивочная PF-12 CNK', 'Скоба обивочная PF-12 CNK', 'Скоба обивочная PF-14 CNK', 'Скоба обивочная PF-14 CNK', 'Скоба для степлера 140/06 (140)', 'Скоба для степлера 140/06 (140)', 'Скоба для степлера 140/08 (140)', 'Скоба для степлера 140/08 (140)', 'Скоба для степлера 140/10 (140)', 'Скоба для степлера 140/10 (140)', 'Скоба для степлера 140/12 (140)', 'Скоба для степлера 140/12 (140)', 'Скоба для степлера 140/14 (140)', 'Скоба для степлера 140/14 (140)', 'Скоба 53/06В (53)', 'Скоба 53/06В (53)'], ['25,60', '26,12', '28,48', '32,84', '37,57', '42,30', '46,85', '385,19', '418,52', '445,68', '59,41', '70,62', '85,43', '98,42', '81,35', '87,61', '98,57', '107,69', '118,64', '58,42']]
name_array = ['Скоба обивочная А-04cnk (80/04)', 'Скоба обивочная А-04cnk (80/04)', 'Скоба обивочная А-06 cnk (80/06)', 'Скоба обивочная А-06 cnk (80/06)', 'Скоба обивочная А-08 cnk (80/08)', 'Скоба обивочная А-08 cnk (80/08)', 'Скоба обивочная А-10 cnk (80/10)', 'Скоба обивочная А-10 cnk (80/10)', 'Скоба обивочная А-12 cnk (80/12)', 'Скоба обивочная А-12 cnk (80/12)', 'Скоба обивочная А-14 cnk (80/14)', 'Скоба обивочная А-14 cnk (80/14)', 'Скоба обивочная А-16 cnk (80/16)', 'Скоба обивочная А-16 cnk (80/16)', 'Скоба обивочная А-06 CRF', 'Скоба обивочная А-06 CRF', 'Скоба обивочная А-08 CRF', 'Скоба обивочная А-08 CRF', 'Скоба обивочная А-10 CRF', 'Скоба обивочная А-10 CRF', 'Скоба обивочная PF-06 CNK', 'Скоба обивочная PF-06 CNK', 'Скоба обивочная PF-09 CNK', 'Скоба обивочная PF-09 CNK', 'Скоба обивочная PF-12 CNK', 'Скоба обивочная PF-12 CNK', 'Скоба обивочная PF-14 CNK', 'Скоба обивочная PF-14 CNK', 'Скоба для степлера 140/06 (140)', 'Скоба для степлера 140/06 (140)', 'Скоба для степлера 140/08 (140)', 'Скоба для степлера 140/08 (140)', 'Скоба для степлера 140/10 (140)', 'Скоба для степлера 140/10 (140)', 'Скоба для степлера 140/12 (140)', 'Скоба для степлера 140/12 (140)', 'Скоба для степлера 140/14 (140)', 'Скоба для степлера 140/14 (140)', 'Скоба 53/06В (53)', 'Скоба 53/06В (53)']
price_array = ['25,60', '26,12', '28,48', '32,84', '37,57', '42,30', '46,85', '385,19', '418,52', '445,68', '59,41', '70,62', '85,43', '98,42', '81,35', '87,61', '98,57', '107,69', '118,64', '58,42']
columns_for_df = ['Дата формирования отчета', 'Группы покупателя', 'Покупатель', 'Номер и дата отгрузки', 'Отсрочка, дней', 'Дней до оплаты', 'Размер просроченной задолженности', 'Статус', 'ссылка на документ']


def send_to_forest_sheet(name_array =[], price_array=[]):
    zipped_data = []
    if len(name_array) == len(price_array):
        for i in range(len(name_array)):
            zipped_data.append([name_array[i], locale.atof(price_array[i])])
    work_forest_book = GoogleBook(parsing_book)
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