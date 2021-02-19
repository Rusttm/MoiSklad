
from bs4 import BeautifulSoup
import requests
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

url='https://www.for-est.ru/catalog/krepezh/skoby/karkasnye/?PAGEN_1=2'
url2='https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/?PAGEN_1=1'

response = requests.get(url)
page = BeautifulSoup(response.text, 'html.parser')
print(page.title)