import requests
import json
from base64 import b64encode
from datetime import datetime
from openpyxl import Workbook
import pandas as pd
from datetime import date
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')

URL = conf['MoiSklad']['URL']
URL_TOKEN = conf['MoiSklad']['URL_TOKEN']
URL2 = conf['MoiSklad']['URL2']
access_token = conf['MoiSklad']['access_token']
url_customers = conf['MoiSklad']['url_customers']   # customers list
url_sotr_list = conf['MoiSklad']['url_sotr_list']   # emploee list
url_outinvoices_list = conf['MoiSklad']['url_outinvoices_list']
url_ininvoices_list = conf['MoiSklad']['url_ininvoices_list']
url_priemka_list = conf['MoiSklad']['url_priemka_list']

header_for_token_auth = {'Authorization': 'Bearer %s' % access_token}

def auth_api():

    userAndPass = b64encode(conf['MoiSklad']['log_pass']).decode("ascii") #b"user@outlook.com:12345"
    headers = { 'Authorization': 'Basic %s' % userAndPass }
    req = requests.get(url=URL, headers=headers)  # вариант обычного запроса
    f = open("msanswer.html", "w+")
    f.write(req.text)
    f.close()
    token_req = requests.post(url=URL_TOKEN, headers=headers)  # получаем токен
    return token_req.text

def post_token_api():
    login=conf['MoiSklad']['login']
    password=conf['MoiSklad']['password']
    r = requests.get(url = URL_TOKEN) #вариант обычного запроса
    return r



def get_sotr_list():
    '''write employee list in file .json'''
    req=requests.get(url=url_sotr_list,  headers=header_for_token_auth)
    with open('sotr.json', 'w') as f:
        json.dump(req.json(), f, ensure_ascii=False)
    return req

def get_sotr_data(employee_id=conf['MoiSklad']['my_employee_id']):
    '''write employee data by employee id and writte in file .json'''
    try:
        url_sotr=str(url_sotr_list+'/%s' % employee_id)
        req = requests.get(url=url_sotr, headers=header_for_token_auth)
        file_name=str('sotr_%s.json' % req.json()['firstName'])
        with open(file_name,'w') as f:
            json.dump(req.json(), f, ensure_ascii=False)
        return True
    except Exception:
        print('Error', Exception)
        return False


def get_customers_name(customer_href):
    '''Return customer name'''
    try:
        req=requests.get(url=customer_href, headers=header_for_token_auth)
        with open('customers.json', 'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        return req.json()['name']
    except Exception:
        print('Error', Exception)
        return False

def get_customers_list():
    '''write customer list in file .json'''
    try:
        req=requests.get(url=url_customers, headers=header_for_token_auth)
        with open('customers.json', 'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        return True
    except Exception:
        print('Error', Exception)
        return False

def get_invoice_list():
    '''write invoices list in file .json'''
    try:
        req=requests.get(url=url_outinvoices_list, headers=header_for_token_auth)
        toda_y=str(datetime.now().strftime("%Y_%m_%d"))
        file_name = str('outinvoices_%s.json' % toda_y)
        with open(file_name,'w') as ff:
            json.dump(req.json(), ff, ensure_ascii=False)
        x=req.json()
        write_outinvoices_xls(x, '2021_01_01')
        return True
    except Exception:
        print('Error', Exception)
        return False

def get_priemka_list(from_date='2021-01-01', to_date='2021-02-01'):
    '''write supply list and data in file .   '''
    df = pd.DataFrame(columns=['supplyNum', 'supplyDate', 'supplySum', 'supplyVatSum', 'payNumDate', 'paySum', 'payVat','sf_inNum'])
    df_book = pd.DataFrame(columns=['Номер и дата счета-фактуры продавца',
                                    'Номер и дата исправления счета-фактуры продавца',
                                    'Номер и дата корректировочного счета-фактуры продавца',
                                    'Номер и дата исправления корректировочного счета-фактуры продавца',
                                    'Номер и дата документа, подтверждающего уплату налога',
                                    'Дата принятия на учет товаров (работ, услуг), имущественных прав',
                                    'Наименование продавца',
                                    'ИНН/КПП продавца',
                                    'Страна происхождения товара. Номер таможенной декларации',
                                    'Наиме-нование и код валюты',
                                    'Всего покупок, включая НДС',
                                    'сумма НДС',
                                    'покупки, освобождаемые от налога'])


    supplies=requests.get(url=url_priemka_list,  headers=header_for_token_auth)
    with open('supply.json', 'w') as f:
        json.dump(supplies.json(), f, ensure_ascii=False)

    #  get data from   req.json()
    for supply in supplies.json()['rows']:
        try:
            '''work with schet-fakture inner'''
            hreff = supply['factureIn']['meta']['href'] #link to facturein
            infacture = requests.get(url=hreff, headers=header_for_token_auth) #get the json from link
            insf=infacture.json()
            insf_num=str(insf['name']) #get number of facture in
            #insf_date_temp = str(insf['moment']) #get date of facture in
            insf_date =str(datetime.strptime(str(insf['moment']),"%Y-%m-%d %H:%M:%S.%f").date())#get date of facture in and convert only date
            insf_sum = str(insf['sum']) #get summ of facture in
            insf_supplier_date=str(datetime.strptime(str(insf['incomingDate']),"%Y-%m-%d %H:%M:%S.%f").date())
            insf_supplier = str('№'+insf['incomingNumber'] + ' от ' + insf_supplier_date)

            '''work with supplier data'''
            supplier_link=supply['agent']['meta']['href']
            supplier=requests.get(url=supplier_link, headers=header_for_token_auth)
            supplier_data=supplier.json()
            supplier_name=supplier_data['name']
            supplier_inn_kpp=str(supplier_data['inn']+'/'+supplier_data['kpp'])




            '''work with supply data'''
            supply_payed_sum=str(supply['payedSum']) #get summ of supply
            sf_print=str('входная СФ ' +str(insf_num) + ' от ' +str(insf_date) +  ' на сумму ' + insf_sum)
            supply_date=str(datetime.strptime(str(supply['moment']),"%Y-%m-%d %H:%M:%S.%f").date())
            supply_print=str('Приемка '+str(supply['name'])+' от '+ supply_date +' на сумму '+ str(supply['sum']) +' НДС='+str(supply['vatSum']))
            supply_sum=int(supply['sum'])/100
            supply_vat_sum=int(supply['vatSum'])/100

            '''work with payments data'''
            payments_print=str(' Оплачено ' + supply_payed_sum)
            #print(supply_print  + ' '+ sf_print + payments_print)
            payments_total = 0
            payments_vat_total = 0
            pay_num_date=str()
            for payment in supply['payments']:
                payment_link=payment['meta']['href']
                payment_all_data=requests.get(url=payment_link, headers=header_for_token_auth)
                payment_data=payment_all_data.json()
                pay_num=str(payment_data['name'])
                pay_sum=int(payment_data['sum'])
                pay_vat_sum = int(payment_data['vatSum'])
                pay_date=str(datetime.strptime(str(payment_data['moment']),"%Y-%m-%d %H:%M:%S.%f").date())
                #print('Оплата ' +pay_num + ' от ' + pay_date + ' На сумму ' +str(pay_sum) + ' НДС ' +  str(pay_vat_sum))
                payments_vat_total+=pay_vat_sum
                payments_total+=pay_sum
                pay_num_date+=str('№'+pay_num+' от '+pay_date+' ')
            payments_total=payments_total/100
            payments_vat_total=payments_vat_total/100
            #print('Total  '+ str(payments_total))
            if payments_total>=supply_sum:
                df = df.append(dict(zip(df.columns, ['№'+supply['name'], supply_date, supply_sum, supply_vat_sum, pay_num_date, payments_total, payments_vat_total, '№'+insf_num])), ignore_index=True)
            if supply_vat_sum==0:
                null_vat=supply_sum
                supply_vat_sum='--'
            else: null_vat='--'
            if from_date<=supply_date<=to_date:
                df_book=df_book.append(dict(zip(df_book.columns,
                                            [insf_supplier,
                                             '',
                                             '',
                                             '',
                                             '',
                                             supply_date,
                                             supplier_name,
                                             supplier_inn_kpp,
                                             '--',
                                             'Российский рубль 643',
                                             supply_sum,
                                             supply_vat_sum,
                                             null_vat ])), #корректировать!!!!
                                   ignore_index=True)

        except:
            #print('Приемка '+str(supply['name'])+' от '+str(supply['moment'])+' на сумму '+ str(supply['sum'])+ ' входная сф отсутствует!')
            continue

    print(df)
    today = date.today()
    sheet_name = str(today.strftime("%m-%d-%y"))
    with pd.ExcelWriter('supply_%s.xlsx' % today) as writer:
        df.to_excel(writer, sheet_name=sheet_name)
        df_book.to_excel(writer, sheet_name='покупки')


    return True





def write_outinvoices_xls(data,writedate='2021_01_01'):

    file_name_xls = str('outinvoices_%s.xls' % writedate)
    book = Workbook()
    sheet = book.active
    sheet.append(('Номер сф','Дата сф','Сумма сф','Клиент '))
    for num in data['rows']:
        name_customer=get_customers_name(num['agent']['meta']['href'])
        sheet.append((num['name'],num['moment'],num['sum']/100,name_customer))
    book.save(file_name_xls)
    return True

def test_xls():
    book = Workbook()
    sheet = book.active
    for i in range(10):
        sheet.append((i,i*i))
    book.save('test.xls')

def get_dt_purchases(start_date='2021-01-01'):
    today = date.today()
    today_date = str(today.strftime("%Y-%m-%d"))
    request_date=str(datetime.strptime(start_date,"%Y-%m-%d").date())
    get_priemka_list(from_date=request_date, to_date=today_date)


get_dt_purchases()