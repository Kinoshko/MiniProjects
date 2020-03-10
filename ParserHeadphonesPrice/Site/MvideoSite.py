from Site import Website


class MvideoSite(Website):
    def __init__(self):
        super.__init__('Mvideo', 'https://www.mvideo.ru/products/naushniki-bluetooth-sony-wh-1000xm3-black-50124192')

    def parse(self):
        pass