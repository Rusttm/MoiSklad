import urllib3
from bs4 import BeautifulSoup

import pars_sites


def test1():
    url='https://www.pakt-group.ru/catalog/skobi/c1092/?page=2&next=21&lang=ru&webp=1'
    http = urllib3.PoolManager()
    fields = {'page': 2}
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
             'page': 2}
    response= http.request('GET', url, fields=fields, headers=headers)
    soup = BeautifulSoup(response.data, 'lxml')
    quotes_names_block = soup.find_all('div', class_='catalog-model-name catalog-list-tile-name')
    print(len(quotes_names_block), response.status, response.data, response.headers)


print(pars_sites.parsing_serman_site())