
from bs4 import BeautifulSoup
import requests


url = 'https://www.for-est.ru/catalog/krepezh/skoby/karkasnye/?PAGEN_1=2'
url2 = 'https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/?PAGEN_1=1'

response = requests.get(url)
page = BeautifulSoup(response.text, 'html.parser')

print(page.title)
