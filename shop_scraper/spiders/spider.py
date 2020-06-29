import scrapy
import re
import pytesseract
import io
import requests
from PIL import Image



headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
Type = ['skirt', 'pants', 'top']

def CleanPrice(price):
    korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+') 
    parsePrice = re.sub(korean, '', price) 
    parsePrice = re.sub('[-=+,#/\?￦:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', parsePrice)
    return parsePrice

def PrintClothes(shopName, itemUrl, clothesType, name, thumbnail, price, images, domain):
    print("===========================================================================================================")
    print("쇼핑몰 이름 : " + shopName)
    print("아이템 URL : " + itemUrl)
    print("타입 : " + clothesType)
    print("상품명 : "+ name)
    print("썸네일 : " + thumbnail)
    print("가격 : " + price)
    print('상품 이미지URL : ', end='')
    for image in images:
        url = domain + image
        print(url)
    print()
# def AssignClothesType(topUrl, pantsUrl, )
class ChoperSpider(scrapy.Spider):
    name = 'choper'
    allowed_domains = ['choper.kr']
    domain = 'http://www.choper.kr'
    start_urls = [
        "http://www.choper.kr/product/list.html?cate_no=30", #Top
        "http://www.choper.kr/product/list.html?cate_no=244", #Pants
        "http://www.choper.kr/product/list.html?cate_no=252" #Skirt
    ]

    # 카테코리별 마지막 페이지를 파싱한다.
    def parse(self, response):
        # 카테고리별 마지막 페이지
        lastPage = response.css('#contents > div.xans-element-.xans-product.xans-product-normalpaging.ec-base-paginate > p:nth-child(5) > a::attr(href)').extract()[0]
        lastPage = lastPage[lastPage.find('page=') + 5:]
        # 상품별 ItemPath
        for page in range(1, int(lastPage) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url,self.parse_item)
    def parse_item(self, response):
        itemsPath = response.css('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div > p.name > a::attr(href)').extract()
        for itemPath in itemsPath:
            url = self.domain + itemPath
            yield scrapy.Request(url, self.parse_item_info)
    def parse_item_info(self, response):
        shopName = self.name
        itemUrl = response.url
        name = response.xpath('//*[@id="decolay"]/div[1]/h2/text()').extract()[0]
        price = CleanPrice(response.xpath('//*[@id="span_product_price_text"]/text()').extract()[0])
        thumbnail = response.css('#pro_detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > div > a > img::attr(src)').extract()[0]
        images = response.css('#prdDetail > div.cont > p > img::attr(src)').extract()
        if(itemUrl.find('cate_no=252') != -1):
            clothesType = Type[0]
        if(itemUrl.find('cate_no=244') != -1):
            clothesType = Type[1]
        if(itemUrl.find('cate_no=30') != -1):
            clothesType = Type[2]
        domain = self.domain
        PrintClothes(shopName, itemUrl, clothesType, name, thumbnail, price, images, domain)


class OCRSpider(scrapy.Spider):
    name = "ocrtest"
    allowed_domains = ["choper.kr"]
    domain = 'http://www.choper.kr'
    start_urls = [
        "http://www.choper.kr/product/detail.html?product_no=8968&cate_no=30&display_group=1#"
    ]
    def parse(self, response):
        #prdDetail > div.cont > p:nth-child(31) > img
        size = response.xpath('//*[@id="prdDetail"]/div[1]/p/img/@src').extract()[-1]
        sizeUrl = self.domain + size
        res = requests.get(sizeUrl, headers = headers)
        img = Image.open(io.BytesIO(res.content))
        print(pytesseract.image_to_string(img, lang='kor'))

class BenitoSpider(scrapy.Spider):
    name = "benito"
    allowed_domains = ["benito.co.kr"]
    domain = 'https://www.benito.co.kr'
    start_urls = [
        "https://www.benito.co.kr/product/list.html?cate_no=33", #Skirt
        "https://www.benito.co.kr/product/list.html?cate_no=41", #Top
        "https://www.benito.co.kr/product/list.html?cate_no=36", #Pants
    ]
    # 카테고리별 마지막 페이지를 파싱한다.
    def parse(self, response):
        # 카테고리별 마지막 페이지
        lastPage = response.xpath(
            '//*[@id="contents"]/div[5]/a/@href').extract()[-1]
        lastPage = lastPage[lastPage.find('page=') + 5:]
        for page in range(1, int(lastPage) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url,self.parse_item)
    # 한 페이지 내의 모든 item페이지를 파싱한다.
    def parse_item(self, response):
        itemsPath = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/@href').extract()
        for itemPath in itemsPath:
            url = self.domain + itemPath
            yield scrapy.Request(url, self.parse_item_info)
    # 페이지에 들어가서 상세정보, 이미지 파싱한다.
    def parse_item_info(self, response):
        shopName = self.name
        itemUrl = response.url
        name = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[2]/div[1]/h2/text()[1]').extract()[0]
        thumbnail = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[1]/div[1]/div/a/img/@src').extract()[0]
        price = CleanPrice(response.xpath('//*[@id="span_product_price_text"]/text()').extract()[0])
        images = response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div/p/img/@src').extract()
        if(itemUrl.find('/category/33') != -1):
            clothesType = Type[0]
        if(itemUrl.find('/category/36') != -1):
            clothesType = Type[1]
        if(itemUrl.find('/category/41') != -1):
            clothesType = Type[2]
        # domain = self.domain
        domain = ''
        PrintClothes(shopName, itemUrl, clothesType, name, thumbnail, price, images, domain)

class SizeSpider(scrapy.Spider):
    name = "benitosize"
    allowed_domains = ["benito.co.kr"]
    domain = 'https://www.benito.co.kr'
    start_urls = [
        "https://www.benito.co.kr/product/당일발송러빈-오프-니트-3color/13585/category/41/display/1/", #Top
    ]
    def parse(self, response):
        # size = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[2]/div[1]/h2')
        sizeUrl = response.css('iframe::attr(src)').extract()[0]
        yield scrapy.Request(sizeUrl, self.parse_item_size)



