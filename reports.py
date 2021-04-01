"""управленческие отчеты"""
import configparser

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
    saratov_book = conf['GOOGLE']['saratov_book']
    nsk_book = conf['GOOGLE']['nsk_book']
    temp_book = conf['GOOGLE']['temp_book']
    saratov_link = conf['GOOGLE']['saratov_link']
    nsk_link = conf['GOOGLE']['nsk_link']
    CREDENTIALS_FILE = conf['GOOGLE']['CREDENTIALS_FILE']
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
except IndexError:
    print('cant load data from .ini file', Exception)