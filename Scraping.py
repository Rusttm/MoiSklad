import configparser
import requests
import scrapy
from scrapy.http import FormRequest
import urllib3
from urllib3 import PoolManager
import certifi
import urllib.request as urlrq
import ssl
from scrapy.http.cookies import CookieJar



try:
    conf = configparser.ConfigParser()
    conf.read('scraping.ini')
    forest_80 = conf['WEB']['forest_80']
    forest_80_pages = conf['WEB']['forest_80_pages']
except IndexError:
    print('Cant read data from ini file', Exception)

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']




def try_with_scrapy():
    cookie_content = {'BITRIX_SM_SALE_UID': '13563937',
                      '_ym_uid': '1613744621442053727',
                      '_ym_d': '1613744621',
                      'BX_USER_ID': '5bf2aeeb69ae286760077aa5dd08aa44', 'PHPSESSID': 'RV8Lu0AIbJgdn42t3ZluP2CekAFuJOX1',
                      'clicks': 'Y', '_ym_visorc': 'w', '_ym_isad': '2'}
    request_with_cookies = scrapy.Request(url='https://www.for-est.ru', method='GET', cookies=cookie_content)
    #new_cokies = request_with_cookies.headers.getlist('Set-Cookie')
    #request_with_cookies = Request(url='https://www.for-est.ru', cookies=new_cokies)
    print(request_with_cookies)


def try_with_urllib3():
    cookie_content = {'BITRIX_SM_SALE_UID': '13563937',
                      '_ym_uid': '1613744621442053727',
                      '_ym_d': '1613744621',
                      'BX_USER_ID': '5bf2aeeb69ae286760077aa5dd08aa44', 'PHPSESSID': 'RV8Lu0AIbJgdn42t3ZluP2CekAFuJOX1',
                      'clicks': 'Y', '_ym_visorc': 'w', '_ym_isad': '2'}

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    cookies2 = response.headers.getlist('Set-Cookie')
    r = http.request( 'POST', url='https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/?PAGEN_1=1', cookies=cookies2)
    print(r.data)

def try_with_requests():
    url = forest_80
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    cookie_content = {'BITRIX_SM_SALE_UID': '13563937',
                      '_ym_uid': '1613744621442053727',
                      '_ym_d': '1613744621',
                      'BX_USER_ID': '5bf2aeeb69ae286760077aa5dd08aa44', 'PHPSESSID': 'RV8Lu0AIbJgdn42t3ZluP2CekAFuJOX1',
                      'clicks': 'Y', '_ym_visorc': 'w', '_ym_isad': '2'}

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    req = session.get(url, verify=False)
    post_response = session.post(url, json=cookie_content, verify=False )
    #print(req.content)
    print(post_response.text)
    #r = requests.get(url, headers=headers, cert=certifi.where())
    #print(post_response.text)
    #with open('test.html', 'w') as output_file:
      #output_file.write(req.text.encode('cp1251'))


def try_with_cookies():
    url = 'https://www.for-est.ru/'
    r = requests.get(url)
    r.cookies

