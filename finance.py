import configparser
import pathlib
import requests
import json
from base64 import b64encode
from datetime import datetime
import xlsxwriter
import pandas as pd
from datetime import date

try:
    #get data from in file
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
    url_customers = conf['MoiSklad']['url_customers']
except:
    print('Error, cant read in file')

today = date.today()
today_date = str(today.strftime("%d-%m-%y"))


def ini_file_write(file_name='finance.ini' , tree='MoiSklad', section='account', entry='0'):
    '''this function write data to ini file'''
    try:
        ini_file = pathlib.Path(file_name)
        config = configparser.ConfigParser()
        config.read(ini_file)
        config.set(tree, section, entry)
        config.write(ini_file.open("w"))
    except:
        print('ini file hasnt updated')

def get_account_summ():
    try:
        acc_req = requests.get(url=url_money, headers=header_for_token_auth)
        #with open('money_req_list.json', 'w') as ff:
        #    json.dump(acc_req.json(), ff, ensure_ascii=False)
        acc_2_3_sum=acc_req.json()['rows'][2]['balance']+acc_req.json()['rows'][2]['balance']
        account_sum=str(acc_2_3_sum)
        ini_file_write('finance.ini', 'MoiSklad', 'account_sum', account_sum)  # write data to finance.ini file
        ini_file_write('finance.ini', 'MoiSklad', 'account_date', today_date)
        ini_file_write('bot.ini', 'MoiSklad', 'account_sum', account_sum)
        ini_file_write('bot.ini', 'MoiSklad', 'account_date', today_date)
        return True
    except:
        print('Cant read account data')
        return False



#ini_file_write('finance.ini', 'MoiSklad', 'account', '0') #write data to finance.ini file
get_account_summ()