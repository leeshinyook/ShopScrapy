import re


def clean_price(price):
    korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    english = re.compile('[A-Za-z]')
    special_char = re.compile('[-=+,#/\?￦:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]')
    parse_price = re.sub(korean, '', price)
    parse_price = re.sub(english, '', parse_price)
    parse_price = re.sub(special_char, '', parse_price)
    return parse_price.strip()


def print_clothes(shop_name, domain, item_url, name, thumbnail, price, size_image, size_text):
    print("===========================================================================================================")
    print("쇼핑몰 이름 : " + shop_name)
    print("쇼핑몰 도메인 : " + domain)
    print("아이템 URL : " + item_url)
    print("상품명 : " + name)
    print("썸네일 : " + thumbnail)
    print("가격 : " + price)
    print("사이즈 이미지 : " + size_image)
    print("사이즈 텍스트 : " + str(size_text))
    print()