import scrapy
import re

class SP2Spider(scrapy.Spider):
    name = 'git'
    allowed_domains = ['github.com']
    start_urls = [
        "https://github.com/leeshinyook"
    ]

    def parse(self, response):
        print(response)


class SPSpider(scrapy.Spider):
    name = "benito"
    allowed_domains = ["benito.co.kr"]
    start_urls = [
        "https://www.benito.co.kr/product/list.html?cate_no=33", #Skirt
        "https://www.benito.co.kr/product/list.html?cate_no=36", #Pants
        "https://www.benito.co.kr/product/list.html?cate_no=41", #Top
    ]

    # 카테고리별 마지막 페이지를 파싱한다.
    def parse(self, response):
        # 카테고리별 마지막 페이지
        lastPage = response.xpath(
            '//*[@id="contents"]/div[5]/a/@href').extract()[-1]
        lastPage = lastPage[lastPage.find('page=') + 5:]
        # 상품별 ItemPath
        itemPath = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/@href').extract()
        for page in range(1, int(lastPage) + 1):
            url = response.url + "&page=" + str(page)
            yield scrapy.Request(url,self.parse_item)
    # 한 페이지 내의 모든 item페이지를 파싱한다.
    def parse_item(self, response):
        itemsPath = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/@href').extract()
        for itemPath in itemsPath:
            url = "https://www.benito.co.kr" + itemPath
            # print(url)
            yield scrapy.Request(url, self.parse_item_info)
        # yield scrapy.Request('https://www.benito.co.kr/product/랄프-스커트-2color/13252/category/33/display/1/', self.parse_item_info)
    # 페이지에 들어가서 상세정보, 이미지 파싱한다.
    def parse_item_info(self, response):
        print("===========================================================================================================s")
        itemUrl = response.url
        name = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[2]/div[1]/h2/text()[1]').extract()[0]
        thumbnail = response.xpath('//*[@id="contents"]/div[1]/div[1]/div[1]/div[1]/div/a/img/@src').extract()[0]
        price = response.xpath('//*[@id="span_product_price_text"]/text()').extract()[0]
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
        parsePrice = re.sub(korean, '', price)
        images = response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div/p/img/@src').extract()
        if(itemUrl.find('/category/33')):
            clothesType = 'skirt'
        if(itemUrl.find('/category/36')):
            clothesType = 'pants'
        if(itemUrl.find('/category/41')):
            clothesType = 'top'
        print("아이템 URL : " + itemUrl)
        print("타입 : " + clothesType)
        print("상품명 : "+ name)
        print("썸네일 : " + thumbnail)
        print("가격 : " + parsePrice)
        print('상품 이미지URL : ', end='')
        for image in images:
            url = "https://www.benito.co.kr" + image
            print(url)