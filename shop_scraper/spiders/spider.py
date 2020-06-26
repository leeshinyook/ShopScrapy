import scrapy


# class SP2Spider(scrapy.Spider):


class SPSpider(scrapy.Spider):
    name = "benito"
    allowed_domains = ["benito.co.kr"]
    start_urls = [
        "https://www.benito.co.kr/product/list.html?cate_no=33"
    ]

    def parse(self, response):
        # 카테고리별 마지막 페이지
        lastPage = response.xpath(
            '//*[@id="contents"]/div[5]/a/@href').extract()[-1]
        lastPage = lastPage[lastPage.find('page=') + 5:]
        itemPath = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/@href').extract()
        imagePath = response.xpath(
            '/html/body/div[2]/div[2]/div/div[4]/div[2]/ul/li/div/a/img/@ec-data-src').extract()
        print(imagePath)
