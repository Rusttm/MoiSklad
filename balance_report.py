""" балансовый отчет """
import configparser
import requests
import os
import json
import datetime
import SermanGB

try:
    # get data from ini file
    conf = configparser.ConfigParser()
    conf.optionxform = str
    conf.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))
    url_money = conf['MoiSklad']['url_money']
    url_store_all = conf['MoiSklad']['url_store_all']
    url_stores = conf['MoiSklad']['url_stores']
    url_customers2 = conf['MoiSklad']['url_customers2']
    my_access_token = conf['MoiSklad']['access_token']
    header_for_token_auth = {'Authorization': 'Bearer %s' % my_access_token}
    # эта часть кода позволяет использовать несколько заголовков
    url_headers = conf['API_HEADERS']
    headers_dict = dict()
    for header in url_headers:
        headers_dict[header] = url_headers[header]
    header_for_token_auth = headers_dict
    #
except Exception as m:
    print('Error, cant read .ini file', m)

class serman_balance():
    def __init__(self):
        self.account_bal= 0
        #exchange cources - deprecated
        self.account_exch = {'40702840997960000004': 1, '40702156997960000002': 1}
        self.store_bal = 0
        self.good = {}
        self.stocks = {}
        self.excluded = ['Склад Гарантия', 'Склад Гарантия']
        self.excluded_groups = ['офис поставщики', 'банки', 'транспорт']
        self.customers_groups = {}
        self.custm_bal = []
        self.final_list = []
        self.data_string = []
        self.cont_transport = ['ПАО "ТРАНСКОНТЕЙНЕР"', 'ФТС России', 'ООО "ТРАСКО"', 'ООО "МЕДИТЕРРАНЕАН ШИППИНГ КОМПАНИ РУСЬ"']

        #arrange method for customers
        self.customers_shape = ['поставщики', 'новосибирскконтрагенты', 'москваконтрагенты', 'покупатели пфо', 'транспорт', 'офис поставщики']

    def send_balance_to_GB(self):
        self.get_balance()
        try:
            x=[self.data_string]
            book = SermanGB.ServiceGoogleBook(work_book='balance_book')
            req = book.append_string(work_array=x, sheetId=0)
            return [self.data_string[1], req]
        except Exception as m:
            print('balance hadnt send to Goggle Books:', m)

    def get_balance(self):

        self.account_summ()
        self.store_remains()
        self.customers_bal()
        self.final_list.append(['деньги на счетах', self.account_bal])
        self.final_list.append(['склад себестоимость', self.store_bal])
        self.final_list += self.custm_bal
        summary_balance = 0
        for name, summ in self.final_list:
            summary_balance += summ
        today = datetime.datetime.now()
        today_date = str(today.strftime("%d.%m.%y %H:%M"))
        self.final_list = [['Дата', today_date], ['Итог', int(summary_balance)]] + self.final_list
        for title, summ in self.final_list:
            self.data_string.append(summ)
        return self.data_string[1]

    def account_summ(self):
        """'''this function gets bank account remains'''"""
        # выает сумму на счетах компании
        try:
            acc_req = requests.get(url=url_money, headers=header_for_token_auth)
            # with open('money_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            for account in acc_req.json()['rows']:
                try:
                    acc_name = account['account']['name']
                    acc_courses = self.account_exch
                    if acc_name in acc_courses.keys():
                        self.account_bal += account['balance'] * acc_courses[acc_name] / 100
                    else:
                        self.account_bal += account['balance']/100
                except:
                    self.account_bal += account['balance'] / 100
        except IndexError:
            print('Cant read account data', Exception)
        #print(f'account_sum_ready')
        #print(self.account_bal)

    def store_remains(self):
        """'''this function gets good's price and stock remains'''"""
        try:
            # lets made the price dictionary
            acc_req = requests.get(url=f'{url_store_all}?filter=quantityMode=all', headers=header_for_token_auth)
            # with open('store_all_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            for good in acc_req.json()['rows']:
                self.good[good['meta']['href']] = good['price']/100
            #     self.store += account['balance'] / 100
        except IndexError:
            print('Cant read price data', Exception)
        #print(f'goods_price_ready')

        try:
            # lets made and fill the stock sum dictionary
            acc_req = requests.get(url=url_stores, headers=header_for_token_auth)
            # with open('stores_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            for good in acc_req.json()['rows']:
                good_name = good['meta']['href']
                try:
                    good_price = self.good[good_name]
                except:
                    good_price = 0
                    print(f'{good_name} is not in json all')
                for stock in good['stockByStore']:
                    stock_name = stock['name']
                    stock_num = stock['stock']
                    self.stocks[stock_name] = stock_num*good_price + self.stocks.get(stock_name, 0)
        except IndexError:
            print('Cant read stocks data', Exception)
        #print(f'stocks_price_ready')

        # lets count
        try:
            for stock, summ in self.stocks.items():
                if stock not in self.excluded:
                    self.store_bal += int(summ)
        except:
            print('Cant count stocks sum')
        #print(self.store_bal)

    def customers_bal(self):
        """'''this function gets account remains'''"""
        try:
            url = url_customers2 + '?filter=balance!=0'
            acc_req = requests.get(url=url, headers=header_for_token_auth)
            # with open('customers_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            for customer in acc_req.json()['rows']:
                customer_name = customer['counterparty']['name']
                customer_bal = customer['balance']/100
                customer_href = customer['counterparty']['meta']['href']
                # запрашиваем данные по клиенту
                sub_req = requests.get(url=customer_href, headers=header_for_token_auth)
                # будем формировать список групп для клиента
                customer_groups = []
                try:
                    for group in sub_req.json()['tags']:
                        customer_groups.append(group)
                        self.customers_groups.setdefault(group, 0)

                    # if you have customer has >1 groups
                    if len(customer_groups) > 1:
                        print(f'{customer_name} have {len(customer_groups)} groups')
                    else:
                        # исключаем офисных и лишний транспорт кроме контейнерных
                        if group not in ['транспорт', 'офис поставщики'] or customer_name in self.cont_transport:
                            # прибавляем баланс клиента к общей сумме
                            self.customers_groups[customer_groups[0]] += int(customer_bal)

                except:
                    print(f'{customer_name} has no group')

        except Exception as m:
            print('Cant read account data', m)

      #arrange list
        for group_name in self.customers_shape:
            try:
                summ = self.customers_groups.pop(group_name)
            except:
                summ = 0
            self.custm_bal.append([group_name, -summ])


def new_balance_report():
    my_balance_report = serman_balance()
    return my_balance_report.send_balance_to_GB()


#my_balance_report = serman_balance()
# my_balance_report.account_summ()
# my_balance_report.store_remains()
#my_balance_report.customers_bal()
#print(my_balance_report.send_balance_to_GB())


if __name__ == "__main__":
    new_balance_report()