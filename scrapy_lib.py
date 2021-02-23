import scrapy
from google_books import send_to_forest

class BrickSetSpider(scrapy.Spider):
    name = "forest_spider"
    start_urls = ['https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/']

    def parse(self, response):
        names = response.xpath('//div[@class = "desc_name"]/a/text()').extract()
        prices = response.xpath('//div[@class = "price"]/span/text()').extract()
        print(names, prices)
        send_to_forest(names, prices)