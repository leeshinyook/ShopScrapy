# aftermonday = {
#         "name": "aftermonday",
#         "allowed_domains": ["aftermonday.com"],
#         "domain": "http://aftermonday.com",
#         "start_urls": [
#             "http://aftermonday.com/shop/shopbrand.html?xcode=033&mcode=004&type=Y"
#         ],
#         "xpath_args": {
#             "last_page": """
#             //*[@id="paging"]/p[2]/a/@href
#             """,
#             "last_page_qs": "page=",
#             "items": """//*[@id="gbody"]/div/div[3]/ul/li/a/@href""",
#             "thumbnail": """//*[@id="productDetail"]/img/@src""",
#             "name": """//*[@id="form1"]/div/p[1]/span/text()""",
#             "price": """//*[@id="span_product_price_text"]/text()""",
#             "size_image": "",
#             "image_url": """""",
#             "size_iframe_url": """/html/body/div[4]/div/div[4]/div[1]/div[3]/iframe/@src""",
#             "size_text": "",
#             "product_id": ""
#         }
# }
ggsing = {
    "name": "ggsing",
    "allowed_domains": ["ggsing.com"],
    "domain": "http://www.ggsing.com",
    "start_urls": [
            """https://ggsing.com/product/list.html?cate_no=47#accNav_b']"""
    ],
    "xpath_args": {
        "last_page": """
            //*[@id="contents"]/div[5]/ol/li/a/@href
            """,
        "last_page_qs": "page=",
        "items": """/html/body/div[3]/div[2]/div[2]/div[4]/ul/li/div[1]/a/@href""",
        "thumbnail": """//*[@id="contents"]/div[2]/div[1]/div[1]/div[1]/a/img/@src""",
        "name": """/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/h3/text()""",
        "price": """//*[@id="span_product_price_text"]/text()""",
        "size_image": "",
        "image_url": """//*[@id="product_detail"]/img[7]/@ec-data-src""",
        "size_iframe_url": """/html/body/div[3]/div[2]/div[2]/div[7]/div[2]/div/div[2]/img/@src""",
        "size_text": "",
        "product_id": ""
    }
}

blackup = {
    "name": "blackup",
    "allowed_domains": ["black-up.kr"],
    "domain": "http://black-up.kr",
    "start_urls": [
            """http://black-up.kr/category/top/25']"""
    ],
    "xpath_args": {
        "last_page": """
            //*[@id="contents_wide"]/div[5]/a[4]/@href
            """,
        "last_page_qs": "page=",
        "items": """/ html / body / div[2] / div[2] / div / div[4] / div[2] / ul / li / div[1] / a/@href""",
        "thumbnail": """/ html / body / div[2] / div[2] / div / div[1] / div[1] / div[1] / div[1] / div[1] / div / img/@src""",
        "name": """//*[@id="bu_contents"]/div[1]/div[1]/div[2]/div[1]/h3/text()""",
        "price": """//*[@id="span_product_price_text"]/text()""",
        "size_image": "",
        "image_url": """//*[@id="prdDetail"]/div[2]/img[3]/@ec-data-src""",
        "size_iframe_url": """//*[@id="prdDetail"]/div/iframe/@src""",
        "size_text": "",
        "product_id": ""
    }
}

shop_list = [
    blackup,
    ggsing
]
