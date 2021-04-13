import scrapy
import google_books


class ForestSpider(scrapy.Spider):
    name = "forest_spider"
    start_urls = ['https://www.for-est.ru/catalog/skoby/obivochnye/',  'https://www.for-est.ru/catalog/krepezh/skoby/obivochnye/',
                  'https://www.for-est.ru/catalog/skoby/karkasnye/', 'https://www.for-est.ru/catalog/krepezh/skoby/karkasnye/']

    def parse(self, response):
        names = response.xpath('//div[@class = "description"]/div[@class = "desc_name"]/a/text()').extract()
        prices = response.xpath('//div[@class = "price"]/span/text()').extract()
        print(google_books.send_to_forest_sheet(names, prices))
        next_page = response.xpath('//a[@class = "arrow right"]/@href').extract_first()
        print('результат запроса -', next_page)
        if next_page:
            """run new page search"""
            print('moving to next page', next_page)
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        print('Thats ALL!!!')
