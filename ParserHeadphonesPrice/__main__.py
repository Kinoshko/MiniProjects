import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import re
import smtplib
from configparser import ConfigParser
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from Site.DrHeadSite import DrHeadSite
import json


def send_mail(login: str, password: str, recipients: List[str], message: str, subject: str):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'Python scipt <' + login + '>'
    msg['To'] = ','.join(recipients)

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL(server_mail)
    server.login(login, password)
    server.sendmail(login, recipients, msg.as_string())
    server.quit()


def get_html(url: str, headers: Dict[str, str], params=None):
    request = requests.get(url, headers=headers, params=params)
    print(request.status_code)
    if request.status_code == 200:
        return request.text
    return 'Error'


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='dp_cur_price')
    return int(re.sub(r'[\.!– \-@#$%^&*()|/"\']', '', items.get_text()))


if __name__ == '__main__':
    if os.path.exists('config.ini'):
        config = ConfigParser()
        config.read('config.ini')
        login = config.get('Authentication', 'login')
        password = config.get('Authentication', 'password')
    else:
        raise FileNotFoundError('no exists config.ini')

    if not os.path.exists('prices.json'):
        file = open('prices.json', 'w')
        file.close()

    sites = [DrHeadSite()]

    server_mail = 'smtp.gmail.com'

    recipients = ['v.bityukov94@yandex.ru']

    # HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                         ' Chrome/79.0.3945.130 Safari/537.36', 'accept': '*/*'}
    # url = {'doctorhead': 'https://doctorhead.ru/product/sony_wh_1000xm3_black/',
    #       'mvideo': 'https://www.mvideo.ru/products/naushniki-bluetooth-sony-wh-1000xm3-black-50124192'}
    while True:
        for site in sites:
            current_price = site.parse()

            with open('prices.json', 'r', encoding='utf-8') as file_handler:
                try:
                    prices = json.load(file_handler)
                except Exception:
                    prices = {}

            if site.name not in prices:
                prices[site.name] = current_price
                with open('prices.json', 'w', encoding='utf-8') as file_handler:
                    file_handler.write(json.dumps(prices, ensure_ascii=False))

            if current_price != prices[site.name]:
                prices[site.name] = current_price
                with open('prices.json', 'w', encoding='utf-8') as file_handler:
                    file_handler.write(json.dumps(prices, ensure_ascii=False))
                body = str(current_price)
                send_mail(login, password, recipients, body, 'price of headphones')

        time.sleep(3600)