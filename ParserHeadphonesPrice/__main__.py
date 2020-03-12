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
from Site import DrHeadSite, MvideoSite
import json


def send_mail(login: str, password: str, recipients: List[str], message: str, subject: str):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'Python scipt <' + login + '>'
    msg['To'] = ','.join(recipients)

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login(login, password)
    server.sendmail(login, recipients, msg.as_string())
    server.quit()


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

    sites = [DrHeadSite(), MvideoSite()]
    recipients = ['v.bityukov94@yandex.ru']

    while True:
        price_is_changed = False

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
                price_is_changed = True
        if price_is_changed:
            body = ''
            for s in sites:
                body += f'{prices[s.name]} {s.name} {s.url} \n'
            send_mail(login, password, recipients, body, 'price of headphones')

        time.sleep(3600)