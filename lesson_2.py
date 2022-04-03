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
    clicks_count = requests.get(request_url, headers=requests_headers, params={'units': -1})
    clicks_count.raise_for_status()
    response = f"Данной ссылкой воспользовались {clicks_count.json()['total_clicks']} раз"
    return response

def is_bitlink(url):
    url = urlparse(url)
    if url.netloc == 'bit.ly':
        return True
    return False
    
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    url = input('Введите ссылку: ')
    try:
        if is_bitlink(url):
            print(count_clicks(TOKEN, url))
        else:
            print(shorten_link(TOKEN, url))
    except requests.exceptions.HTTPError:
        print('Введённая ссылка невалидна')
    except:
        print('Что-то пошло не так')
