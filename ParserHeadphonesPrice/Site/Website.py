from abc import ABCMeta, abstractmethod
import requests


class Website(metaclass=ABCMeta):

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/79.0.3945.130 Safari/537.36', 'accept': '*/*'}

    def get_html(self, params=None):
        request = requests.get(self.url, headers=self.headers, params=params)
        if request.status_code == 200:
            return request.text
        return 'Error'  # TODO: add exception

    @abstractmethod
    def parse(self):
        pass
