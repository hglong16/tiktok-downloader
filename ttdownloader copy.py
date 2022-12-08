import requests
from bs4 import BeautifulSoup

url = "https://www.tiktok.com/@thaovy1590/video/7164747239729024282"


def ttdownloader(url):
    try:
        data = requests.get('https://ttdownloader.com/')

        cookie = data.headers['Set-Cookie']

        soup = BeautifulSoup(data.text, 'html.parser')
        token = soup.find('input', {'id': 'token'})['value']
        data_post = {
            'url': url,
            'format': '',
            'token': token
        }

        data = requests.post('https://ttdownloader.com/search/', headers={
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'cookie': cookie
        }, data=data_post)
        soup = BeautifulSoup(data.text, 'html.parser')
        nowm = soup.find('div', {'class': 'download'}).find('a')['href']
        wm = soup.find('div', {'class': 'download'}).find('a')['href']
        audio = soup.find('div', {'class': 'download'}).find('a')['href']

        return {
            'nowm': nowm,
            'wm': wm,
            'audio': audio
        }

    except Exception as e:
        print(e)


print(ttdownloader(url))
