import scrapy
from shop_scraper.spiders.formatter import *
from shop_scraper.spiders.shop.shop import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shop_scraper.spiders.crop import *

def shop_xpath_crawler(passed_name, passed_allowed_domains, passed_domain, passed_start_urls, passed_xpath_args):
    class XPathSpider(scrapy.Spider):
        name = passed_name
        allowed_domains = passed_allowed_domains
        domain = passed_domain
        start_urls = passed_start_urls
        xpath_args = passed_xpath_args

        def parse(self, response):
            last_page = response.xpath(self.xpath_args['last_page']).extract()[-1]
            last_page = last_page[
                        last_page.find(self.xpath_args['last_page_qs']) + len(self.xpath_args['last_page_qs']):]
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
            image_pixel_location = 'None'

            shop_name = self.name
            item_url = response.url
            name = response.xpath(self.xpath_args['name']).extract()[0]
            thumbnail = response.xpath(self.xpath_args['thumbnail']).extract()[0]
            price = clean_price(response.xpath(self.xpath_args['price']).extract()[0])
            domain = self.domain
            image_url = response.xpath(self.xpath_args['image_url']).extract()
            if image_url :
                image_url = clean_url(image_url[0], domain)
                image_pixel_location = find_images_location_from_url(image_url)
            else :
                image_url = 'None'
            # if len(self.xpath_args['size_image']):
            #     size_image = response.xpath(self.xpath_args['size_image']).extract()[-1]
            # else:
            #     size_text = response.xpath(self.xpath_args['size_iframe_url']).extract()[0]
            print_clothes(shop_name, domain, item_url, name, thumbnail, price, size_image, size_text, image_url, image_pixel_location)

    return XPathSpider


for shop in shop_list:
    shop_element = shop_xpath_crawler(
        shop["name"],
        shop["allowed_domains"],
        shop["domain"],
        shop["start_urls"],
        shop["xpath_args"]
    )
    process = CrawlerProcess(get_project_settings())
    process.crawl(shop_element)
process.start(stop_after_crawl=False)
