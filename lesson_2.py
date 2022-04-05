import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

def shorten_link(token, url):
    request_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    requests_headers = {'Authorization': f'Bearer {token}'}
    request_data = {'long_url': url}
    response = requests.post(request_url, headers=requests_headers, json=request_data)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(token, link:str):
    link = urlparse(link)
    formated_link = link.netloc + link.path
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{formated_link}/clicks/summary'
    requests_headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(request_url, headers=requests_headers, params={'units': -1})
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count

def is_bitlink(url, token):
    '''Функция делает запрос на указанный url чтобы убедится в его валидности, 
       а после делает запрос к API сервиса, чтобы узнать, является ли url уже 
       сокращенной ссылкой'''
    requests_headers = {'Authorization': f'Bearer {token}'}
    check_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    response = requests.get(url)
    response.raise_for_status()
    url = urlparse(url)
    bitlink = f'{url.netloc}{url.path}'
    response = requests.get(check_url.format(bitlink), headers=requests_headers)
    return response.ok

    
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("BITLY_TOKEN")
    url = input('Введите ссылку: ')
    try:
        if is_bitlink(url, TOKEN):
            click_count = count_clicks(TOKEN, url)
            print(f"Данной ссылкой воспользовались {click_count} раз")
        else:
            print(shorten_link(TOKEN, url))
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        print('Введённая ссылка невалидна')
    except:
        print('Что-то пошло не так')
