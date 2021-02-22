import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "forest_spider"
    start_urls = ['https://www.for-est.ru/catalog/skoby/obivochnye/']

    def parse(self, response):
        '''
        with open('scrapy_file.txt', 'wb') as f:
            f.write(response.body)
        SET_SELECTOR = '.desc_name'
        for forest in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'a::text'
            #PRICE_SELECTOR = 'span::text'
            yield {'name': forest.css(NAME_SELECTOR).extract_first()}
                   #'price': forest.css(PRICE_SELECTOR).extract_first()}
        '''

        names = response.xpath('//div[@class = "desc_name"]/a/text()').extract()
        prices = response.xpath('//div[@class = "price"]/span/text()').extract()
        filename = '/Volumes/GoogleDrive/My Drive/Python/MoiSklad/MoiSklad/scrapy_file.txt'
        print(names)
        with open(filename, 'w') as f:
            for x in names:
                f.write(x+'\n')

