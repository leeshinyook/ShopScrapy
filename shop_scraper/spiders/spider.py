import scrapy
import re
import pytesseract
import io
import requests
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
Type = ['skirt', 'pants', 'top']


def clean_price(price):
    korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    parse_price = re.sub(korean, '', price)
    parse_price = re.sub('[-=+,#/\?￦:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', parse_price)
    return parse_price


def print_clothes(shop_name, item_url, clothes_type, name, thumbnail, price, images, domain):
    print("===========================================================================================================")
    print("쇼핑몰 이름 : " + shop_name)
    print("아이템 URL : " + item_url)
    print("타입 : " + clothes_type)
    print("상품명 : " + name)
    print("썸네일 : " + thumbnail)
    print("가격 : " + price)
    print('상품 이미지URL : ', end='')
    for image in images:
        url = domain + image
        print(url)
    print()


class ChoperSpider(scrapy.Spider):
    name = 'choper'
    allowed_domains = ['choper.kr']
    domain = 'http://www.choper.kr'
    start_urls = [
        "http://www.choper.kr/product/list.html?cate_no=30",  # Top
        "http://www.choper.kr/product/list.html?cate_no=244",  # Pants
        "http://www.choper.kr/product/list.html?cate_no=252"  # Skirt
    ]

    # 카테코리별 마지막 페이지를 파싱한다.
    def parse(self, response):
        # 카테고리별 마지막 페이지
        last_page = response.css(
            '#contents > div.xans-element-.xans-product.xans-product-normalpaging.ec-base-paginate > p:nth-child(5) > a::attr(href)').extract()[
            0]
        last_page = last_page[last_page.find('page=') + 5:]
        # 상품별 ItemPath
        for page in range(1, int(last_page) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        items_path = response.css(
            '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div > p.name > a::attr(href)').extract()
        for item_path in items_path:
            url = self.domain + item_path
            yield scrapy.Request(url, self.parse_item_info)

    def parse_item_info(self, response):
        global clothes_type
        shop_name = self.name
        item_url = response.url
        name = response.xpath('//*[@id="decolay"]/div[1]/h2/text()').extract()[0]
        price = clean_price(response.xpath('//*[@id="span_product_price_text"]/text()').extract()[0])
        thumbnail = response.css(
            '#pro_detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > div > a > img::attr(src)').extract()[
            0]
        images = response.css('#prdDetail > div.cont > p > img::attr(src)').extract()
        if item_url.find('cate_no=252') != -1:
            clothes_type = Type[0]
        if item_url.find('cate_no=244') != -1:
            clothes_type = Type[1]
        if item_url.find('cate_no=30') != -1:
            clothes_type = Type[2]
        domain = self.domain
        print_clothes(shop_name, item_url, clothes_type, name, thumbnail, price, images, domain)


class OCRSpider(scrapy.Spider):
    name = "ocrtest"
    allowed_domains = ["choper.kr"]
    domain = 'http://www.choper.kr'
    start_urls = [
        "http://www.choper.kr/product/detail.html?product_no=8968&cate_no=30&display_group=1#"
    ]

    def parse(self, response):
        size = response.xpath('//*[@id="prdDetail"]/div[1]/p/img/@src').extract()[-1]
        size_url = self.domain + size
        res = requests.get(size_url, headers=headers)
        img = Image.open(io.BytesIO(res.content))
        print(pytesseract.image_to_string(img, lang='kor'))


class BenitoSpider(scrapy.Spider):
    name = "benito"
    allowed_domains = ["benito.co.kr"]
    domain = 'https://www.benito.co.kr'
    start_urls = [
        "https://www.benito.co.kr/product/list.html?cate_no=33",  # Skirt
        "https://www.benito.co.kr/product/list.html?cate_no=41",  # Top
        "https://www.benito.co.kr/product/list.html?cate_no=36",  # Pants
    ]

    # 카테고리별 마지막 페이지를 파싱한다.
    def parse(self, response):
        # 카테고리별 마지막 페이지
        last_page = response.xpath(
            '//*[@id="contents"]/div[5]/a/@href').extract()[-1]
        last_page = last_page[last_page.find('page=') + 5:]
        for page in range(1, int(last_page) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url, self.parse_item)

    # 한 페이지 내의 모든 item페이지를 파싱한다.
    def parse_item(self, response):
        items_path = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/@href').extract()
        for item_path in items_path:
            url = self.domain + item_path
            yield scrapy.Request(url, self.parse_item_info)

    # 페이지에 들어가서 상세정보, 이미지 파싱한다.
    def parse_item_info(self, response):
        global clothes_type
        shop_name = self.name
        item_url = response.url
        name = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[2]/div[1]/h2/text()[1]').extract()[0]
        thumbnail = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[1]/div[1]/div/a/img/@src').extract()[0]
        price = clean_price(response.xpath('//*[@id="span_product_price_text"]/text()').extract()[0])
        images = response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div/p/img/@src').extract()
        if item_url.find('/category/33') != -1:
            clothes_type = Type[0]
        if item_url.find('/category/36') != -1:
            clothes_type = Type[1]
        if item_url.find('/category/41') != -1:
            clothes_type = Type[2]
        domain = self.domain
        print_clothes(shop_name, item_url, clothes_type, name, thumbnail, price, images, domain)


class SizeSpider(scrapy.Spider):
    name = "benitosize"
    allowed_domains = ["benito.co.kr"]
    domain = 'https://www.benito.co.kr'
    start_urls = [
        "https://www.benito.co.kr/product/당일발송러빈-오프-니트-3color/13585/category/41/display/1/",  # Top
    ]

    def parse(self, response):
        # size = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[2]/div[1]/h2')
        size_url = response.css('iframe::attr(src)').extract()[0]
        yield scrapy.Request(size_url, self.parse_item_size)
