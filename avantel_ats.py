#avantel API


import requests
import configparser
import os


try:
    conf = configparser.ConfigParser()
    #conf.read('avantel.ini')
    conf.read(os.path.join(os.path.dirname(__file__), 'config/avantel.ini'))
except IndexError:
    print('cant find .ini file'), Exception

try:
    token_avantel = conf['ATS']['token_avantel']
    token_ms = conf['ATS']['token_ms']
    link_avantel = conf['ATS']['link_avantel']
    link_ms = conf['ATS']['link_ms']

except IndexError:
    print('cant load data from .ini file', Exception)



def get_the_history():
    header_for_token_auth = {'Authorization': 'Bearer %s' % token_ms}
    headers = token_ms
    data = {'cmd': 'history'}
    req = requests.post(url=link_ms, json=data, headers= headers)
    requests.post
    print(req, req.text)


get_the_history()