from Site import Website
from bs4 import BeautifulSoup
import re


class MvideoSite(Website):
    def __init__(self):
        super().__init__('Mvideo', 'https://www.mvideo.ru/products/naushniki-bluetooth-sony-wh-1000xm3-black-50124192')

    def parse(self):
        html = super().get_html()
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('div', class_='c-pdp-price__current sel-product-tile-price')
        return int(re.sub(r'[\.!–¤\xa0 \-@#$%^&*()|/"\']', '', items.get_text()))
