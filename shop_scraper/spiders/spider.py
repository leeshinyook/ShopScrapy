import scrapy


class SPSpider(scrapy.Spider):
    name = "benito"
    allowed_domains = ["benito.co.kr"]
    start_urls = [
        "https://www.benito.co.kr/product/list.html?cate_no=33"
    ]

    def parse(self, response):
        print(response)
