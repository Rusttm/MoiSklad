import configparser
import pathlib
import requests
from datetime import date



try:
    #get data from in file
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
except:
    print('Error, cant read .ini file')

def get_account_summ():
    '''this function gets account remains'''
    try:
        acc_req = requests.get(url=url_money, headers=header_for_token_auth)
        #with open('money_req_list.json', 'w') as ff:
        #    json.dump(acc_req.json(), ff, ensure_ascii=False)
        acc_2_3_sum=acc_req.json()['rows'][2]['balance']/100+acc_req.json()['rows'][2]['balance']/100
        return acc_2_3_sum
    except:
        print('Cant read account data')
        return 0

