""" остатки по счетам"""
import configparser
import requests
import os

try:
    # get data from in file
    conf = configparser.ConfigParser()
    #conf.read('config.ini')
    conf.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
except IndexError:
    print('Error, cant read .ini file')


def get_account_summ():
    """'''this function gets account remains'''"""

    try:
        acc_req = requests.get(url=url_money, headers=header_for_token_auth)
#        with open('money_req_list.json', 'w') as ff:
        #    json.dump(acc_req.json(), ff, ensure_ascii=False)
        accounts_list = [0]
        for acc in acc_req.json()['rows']:
            accounts_list.append(acc['balance']/100)
            # try:
            #     print(acc['account']['name'], acc['balance']/100)
            # except:
            #     pass
        return sum(accounts_list)
    except IndexError:
        print('Cant read account data', Exception)
        return 0
    print(f'finance report ready')



if __name__ == '__main__':
    print(int(get_account_summ()), 'RUR')