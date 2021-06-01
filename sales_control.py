""" control sales 30% minimum"""
import configparser
import requests
from datetime import date


try:
    # get data from in file
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    URL = conf['MoiSklad']['URL']
    URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
    url_otgruzka_list = conf['MoiSklad']['url_otgruzka_list']
    url_money = conf['MoiSklad']['url_money']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
    url_customers = conf['MoiSklad']['url_customers']
    url_sales_list = conf['MoiSklad']['url_sales_list']
except IndexError:
    print('Error, cant read .ini file', Exception)





def get_sales_list():
    """'''this function gets list of clients with gross efficiency <30% in that day'''"""
    today = date.today()
    today_date = str(today.strftime("%d.%m.%y_%H:%M"))
    today_date_req = str(today.strftime("%Y-%m-%d"))
    failed_sales_list = []
    try:
        sales_req = requests.get(url=f"{url_sales_list}?momentFrom={today_date_req} 00:00:01",
                                 headers=header_for_token_auth)
#        with open('sales_req_list.json', 'w') as ff:
        #    json.dump(sales_req.json(), ff, ensure_ascii=False)
        for client in sales_req.json()['rows']:
            client_name = client['counterparty']['name']
            client_sales = round(client['sellSum']/100, 2)
            client_profit = client['profit']/100
            client_rent = round(client_profit/client_sales, 2)*100
            if client_rent < 30:
                failed_sales_list.append([client_name, client_sales, client_rent])
    except IndexError:
        print('Cant read sales data', Exception)

    return failed_sales_list
