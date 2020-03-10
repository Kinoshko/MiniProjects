from Site import Website
import re
from bs4 import BeautifulSoup


class DrHeadSite(Website):
    def __init__(self):
        super().__init__('DrHead', 'https://doctorhead.ru/product/sony_wh_1000xm3_black/')

    def parse(self):
        html = super().get_html()
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('div', class_='dp_cur_price')
        return int(re.sub(r'[\.!– \-@#$%^&*()|/"\']', '', items.get_text()))
