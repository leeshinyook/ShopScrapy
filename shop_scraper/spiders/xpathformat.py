import scrapy
from shop_scraper.spiders.formatter import *


class XPathSpider(scrapy.Spider):
    name = ''
    allowed_domains = ['']  # ex "benito.co.kr"
    domain = ''  # ex 'https://www.benito.co.kr'
    start_urls = ['']  # ex "https://www.benito.co.kr/product/list.html?cate_no=33"
    xpath_args = {
        'last_page': '',
        'last_page_qs': 'page=',
        'items': '',
        'thumbnail': '',
        'name': '',
        'price': '',
        'size_image': '',
        'size_iframe_url': '',
        'size_text': ''
    }

    def parse(self, response):
        last_page = response.xpath(self.xpath_args['last_page']).extract()[-1]
        last_page = last_page[last_page.find(self.xpath_args['last_page_qs']) + len(self.xpath_args['last_page_qs']):]
        for page in range(1, int(last_page) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        items_path = response.xpath(self.xpath_args['items']).extract()
        for item_path in items_path:
            url = self.domain + item_path
            yield scrapy.Request(url, self.parse_item_info)

    def parse_item_info(self, response):
        size_image = 'None'
        size_text = ''
        shop_name = self.name
        item_url = response.url
        name = response.xpath(self.xpath_args['name']).extract()[0]
        thumbnail = response.xpath(self.xpath_args['thumbnail']).extract()[0]
        price = clean_price(response.xpath(self.xpath_args['price']).extract()[0])
        domain = self.domain
        if len(self.xpath_args['size_image']):
            size_image = response.xpath(self.xpath_args['size_image']).extract()[-1]
        else:
            size_text = response.xpath(self.xpath_args['size_iframe_url']).extract()[0]
        print_clothes(shop_name, domain, item_url, name, thumbnail, price, size_image, size_text)
