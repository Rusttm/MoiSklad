# pars_sites.py
import urllib3
from bs4 import BeautifulSoup
import ssl
import certifi
import xlsxwriter
import service_google_books
import json

import requests
import google_books

#positions dictionary {pos_number: {'staple':'43,4'}}

class pars_serman_site():
    def __init__(self):
        self.links_on_site = ['https://www.sermangroup.ru/catalog/krepezh/skoby/',
                              'https://sermangroup.ru/catalog/instrument/',
                              'https://sermangroup.ru/catalog/aksessuary/']

        self.positions_price = []
        for tag in self.links_on_site:
            self.root_link = tag
            self.last_link = tag
            self.gather_info()

    def take_info_from_link(self):
        """ this function gets link and return list of [price dictionary, next page link]"""
        self.list_price = []
        self.list_names = []
        self.list_links = []
        ssl._create_default_https_context = ssl._create_unverified_context
        #now certificate expired and we use 'CERT_NONE' but must 'CERT_REQUIRED'
        cert_reqs = 'CERT_NONE'
        http = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=certifi.where())
        response = http.request('GET', self.last_link)
        #print(response.status)
        soup = BeautifulSoup(response.data, 'lxml')
        #take name
        quotes_names = soup.find_all('div', class_='title')



        #take price
        quotes_price_text = soup.find_all('div', class_='price bx_price')

        #take next page
        block_link = soup.find_all('div', class_='pager')
        block_soup = BeautifulSoup(str(block_link), 'html.parser')
        list_link = block_soup.find_all('a', href=True)
        try:
            for a in list_link:
                if (a.text == 'Вперёд') and (a['href']!="javascript:void(0)"):
                    # предполагается что на этой кнопке висит ссылка вида /catalog/krepezh/skoby/?PAGEN_1=3&amp;SIZEN_1=12
                    tail = a['href'].split('/')[-1]
                    self.last_link = str(self.root_link + tail)
                    #print(tail)
                    break
                self.last_link = False
        except Exception:
            self.last_link = False
            print('no links forward')

        if len(quotes_names) == len(quotes_price_text):
            for name in quotes_names:
                self.list_names.append(name.text)
                quotes_links = BeautifulSoup(str(name), 'html.parser')
                link = quotes_links.find_all('a', href=True)
                tag = link[0]['href']
                self.list_links.append(f'https://sermangroup.ru{tag}')


            for price_info in quotes_price_text:
                price_string = price_info.text.split()
                if price_string[2] == 'руб.':
                    price = price_string[1]
                    self.list_price.append(float(price))
                elif price_string[3] == 'руб.':
                    price = str(price_string[1] + price_string[2])
                    self.list_price.append(float(price))
        else:
            print('length of name and price are not equant')

        new_pos = list(zip(self.list_names, self.list_price, self.list_links))
        self.positions_price += new_pos

    def gather_info(self):
        while self.last_link:
            self.take_info_from_link()
            #print(self.positions_price)
        print(f'info from Serman site {self.root_link} gathered')

    def fill_the_serman_price(self):
        serman_book = service_google_books.GoogleBook()
        link = serman_book.append_array(work_array=self.positions_price, sheetId='1238490361')
        return link


class pars_forest_site():
    def __init__(self):
        self.links_on_site = ['https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/',
                              'https://www.for-est.ru/catalog/krepezh/skoby/karkasnye/',
                              'https://www.for-est.ru/catalog/krepezh/skoby/upakovochnye/',
                              'https://www.for-est.ru/catalog/krepezh/skoby/spetsialnye/',
                              'https://www.for-est.ru/catalog/instrument/skobozabivnoy/'
                              ]

        self.positions_price = []
        for tag in self.links_on_site:
            self.root_link = tag
            self.last_link = tag
            self.gather_info()

    def take_info_from_link(self):
        """ this function gets link and fill self.positions_price by [(price dictionary, next page link)]"""
        self.list_price = []
        self.list_names = []
        self.list_links = []
        ssl._create_default_https_context = ssl._create_unverified_context
        #now certificate expired and we use 'CERT_NONE' but must 'CERT_REQUIRED'
        cert_reqs = 'CERT_REQUIRED'
        http = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=certifi.where())
        response = http.request('GET', self.last_link)
        #print(response.status)
        soup = BeautifulSoup(response.data, 'lxml')

        #take the name block
        quotes_names_block = soup.find_all('div', class_='description')

        #take the price block
        quotes_price_block = soup.find_all('div', class_='price')



        if len(quotes_names_block) == len(quotes_price_block):
            #pull out names to array
            quotes_names = BeautifulSoup(str(quotes_names_block), 'html.parser')
            quotes_name = quotes_names.find_all('a', href=True)
            for name in quotes_name:
                self.list_names.append(name.text)
                self.list_links.append(f'https://www.for-est.ru{name["href"]}')

            # pull out prices to array
            quotes_prices = BeautifulSoup(str(quotes_price_block), 'html.parser')
            quotes_price = quotes_prices.find_all('span')
            for price1 in quotes_price:
                price_string = price1.text.split()
                if price_string[1] == 'руб.':
                    price = price_string[0]
                    self.list_price.append(price)
                elif price_string[2] == 'руб.':
                    price = str(price_string[0] + price_string[1])
                    self.list_price.append(price)

        else:
            print('length of name and price are not equant')

        #consolidate in array
        new_pos = list(zip(self.list_names, self.list_price, self.list_links))
        self.positions_price += new_pos

        #take info about next page
        block_link = soup.find_all('div', class_='pagination')
        block_soup = BeautifulSoup(str(block_link), 'html.parser')
        next_arrow = block_soup.find_all('a', class_='arrow right')

        #take a tail from
        if next_arrow!=[]:
            x = next_arrow[0]['href']
            tail = x.split('/')[-1]
            self.last_link = str(self.root_link + tail)
        else:
            self.last_link = False
            #print('last page')

    def gather_info(self):
        while self.last_link:
            self.take_info_from_link()
            #print(self.positions_price)
        print(f'info from Forest site {self.root_link} gathered')

    def fill_the_forest_price(self):
        forest_book = service_google_books.GoogleBook()
        link = forest_book.append_array(work_array=self.positions_price, sheetId='0')
        return link


class pars_pakt_site():
    def __init__(self):
        self.links_on_site = ['https://www.pakt-group.ru/catalog/skobi/c1092/',
                              'https://www.pakt-group.ru/catalog/instrument/c1/',
                              'https://www.pakt-group.ru/catalog/aksessuari/c3/'
                              ]

        self.positions_price = []

        for tag in self.links_on_site:
            self.page_num = 1
            self.root_link = tag
            self.last_link = tag
            self.gather_info()


    def take_info_from_link(self):
        """ this function gets link and fill self.positions_price by [(price dictionary, next page link)]"""
        self.list_price = []
        self.list_names = []
        self.list_qty = []
        self.list_links = []
        ssl._create_default_https_context = ssl._create_unverified_context
        # now certificate expired and we use 'CERT_NONE' but must 'CERT_REQUIRED'
        cert_reqs = 'CERT_REQUIRED'
        http = urllib3.PoolManager(cert_reqs=cert_reqs, ca_certs=certifi.where())
        response = http.request('GET', self.last_link)
        #print(response.status)
        #print(self.last_link)
        if response.status == 404:
            self.last_link = False
            return False
        soup = BeautifulSoup(response.data, 'lxml')

        #take positions blocks and information from json
        position_block = soup.find_all('li', class_='lta-item position- image-position-')
        for position in position_block:
            x = json.loads(position['data-layer-list'])
            self.list_names.append(x["name"])
            self.list_price.append(x["price"])
            #get qty type
            pars_block = BeautifulSoup(str(position), 'html.parser')
            qty_name = pars_block.find_all('div', class_="base-unit")
            if qty_name!=[]:
                qty = qty_name[0]
                self.list_qty.append(qty.text)
            else:
                self.list_qty.append('Unknown')
            #get href from position block
            qty_names = pars_block.find_all('a', href=True)
            qty_name = qty_names[0]
            tag = qty_name['href']
            link = f'https://www.pakt-group.ru{tag}'
            self.list_links.append(link)

        # consolidate in array
        new_pos = list(zip(self.list_names, self.list_price, self.list_qty, self.list_links))
        self.positions_price += new_pos
        self.page_num +=1
        # take info about next page
        tail = f'?page={self.page_num}'
        self.last_link = str(self.root_link + tail)
        # if self.page_num < 16:
        #     tail = f'?page={self.page_num}'
        #     self.last_link = str(self.root_link + tail)
        # else:
        #     self.last_link = False
        #     print('last page')


    def gather_info(self):
        while self.last_link:
            self.take_info_from_link()
            #print(self.positions_price[-1])
        print(f'info from Pakt site {self.root_link} gathered')


    def fill_the_pakt_price(self):
        forest_book = service_google_books.GoogleBook()
        link = forest_book.append_array(work_array=self.positions_price, sheetId='374283843')
        return link


def parsing_serman_site():
    x = pars_serman_site()
    return x.fill_the_serman_price()

def parsing_forest_site():
    y = pars_forest_site()
    return y.fill_the_forest_price()

def parsing_pakt_site():
    z = pars_pakt_site()
    return z.fill_the_pakt_price()


#processing

def write_to_sermanfile(data=[(None, None)]):
    workbook = xlsxwriter.Workbook('serman_pars.xlsx')
    worksheet = workbook.add_worksheet('serman')
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num, col_num, col_data)
    workbook.close()

def write_to_paktfile(data=[(None, None)]):
    workbook = xlsxwriter.Workbook('pakt_pars.xlsx')
    worksheet = workbook.add_worksheet('pakt')
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num, col_num, col_data)
    workbook.close()