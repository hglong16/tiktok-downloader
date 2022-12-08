import aiohttp
from bs4 import BeautifulSoup
import asyncio
import aiofiles

url = "https://www.tiktok.com/@thaovy1590/video/7164747239729024282"


async def tt_get_link(url):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://ttdownloader.com/') as response:
            cookie = response.headers['Set-Cookie']
            soup = BeautifulSoup(await response.text(), 'html.parser')
            token = soup.find('input', {'id': 'token'})['value']
        data_post = {
            'url': url,
            'format': '',
            'token': token
        }
        async with session.post('https://ttdownloader.com/search/', headers={
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'cookie': cookie
        }, data=data_post) as res:
            soup2 = BeautifulSoup(await res.text(), 'html.parser')

            if soup2 is not None:

                nowm_class = soup2.find(
                    'a', {'class': 'download-link'})
                if nowm_class is not None:
                    nowm = nowm_class['href']
                    return {
                        'nowm': nowm,
                    }

                print(url, 'soup none')
                print(nowm_class)
                print(res.text())
                return None
            else:
                return None


async def download(id, data, path):
    async with aiohttp.ClientSession() as session:
        if data is not None:
            try:
                async with session.get(data['nowm']) as res:

                    f = await aiofiles.open(f"{path}/{id}.mp4", mode="wb")
                    await f.write(await res.read())
                    await f.close()
            except:
                print('error')
        else:
            print(id, "error")


async def main():
    data = await tt_get_link(url)
    await download(11135, data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
