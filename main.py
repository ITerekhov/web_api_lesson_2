import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

def shorten_link(requests_headers, url):
    request_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    request_data = {'long_url': url}
    response = requests.post(request_url, headers=requests_headers, json=request_data)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(requests_headers, bitlink:str):
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(request_url, headers=requests_headers, params={'units': -1})
    response.raise_for_status()
    return response.json()['total_clicks']

def is_bitlink(requests_headers, bitlink):
    '''Функция делает запрос к API сервиса, чтобы узнать, является ли url уже 
       сокращенной ссылкой'''
    check_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    response = requests.get(check_url.format(bitlink), headers=requests_headers)
    return response.ok

def createParser():
    parser = argparse.ArgumentParser(description='Работа с API сервиса Bitly по сокращению ссылок')
    parser.add_argument('url', help='Ваш Url в формате https://example.com/example_path')
    return parser

def main():
    parser = createParser()
    namespace = parser.parse_args()
    url = namespace.url 
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    requests_headers = {'Authorization': f'Bearer {bitly_token}'}
    try:
        response = requests.get(url)
        response.raise_for_status()
        parsed_url = urlparse(url)
        bitlink = parsed_url.netloc + parsed_url.path
        if is_bitlink(requests_headers, bitlink):
            click_count = count_clicks(requests_headers, bitlink)
            print(f"Данной ссылкой воспользовались {click_count} раз")
        else:
            print(shorten_link(requests_headers, url))
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        print('Введённая ссылка невалидна')

if __name__ == '__main__':
    main()
