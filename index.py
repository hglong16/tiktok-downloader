from TiktokApi import *
import sys
import asyncio
from ttdownloader import tt_get_link, download
from push_db import push_db
import time
import os

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

Api = Tiktok()

# edit username  here
username = 'Đồ tiện ích'
if not os.path.exists(f"./download/{username}"):
    os.makedirs(f"./download/{username}")
path = f"./download/{username}"
url = 'https://tiktok.com/@%s' % username


def genUrl(id):
    return f"https://tiktok.com/@{username}/video/{id}"


Api.openBrowser(url, True)
input('Skip the captcha, press Enter to continue ')
limit = 10000
count = 0
first = True
flag = 0
cursor = 0
secUid = ''
all = []
while True:

    if first == True:
        data = Api.getUserFeed(first=first)
        for x in data['ItemModule']:

            video_id = data['ItemModule'][x]['id']
            caption = data['ItemModule'][x]['desc']
            single_video = data['ItemModule'][x]
            push_db(single_video)
            all.append((video_id, genUrl(video_id)))
            print("Video <<%s>> <<%s>>" %
                  (str(video_id), str(caption)))

            count += 1
            if count == limit:
                flag = 1
                break
        if not data['ItemList']['user-post']['hasMore']:
            break
        cursor = data['ItemList']['user-post']['cursor']
        secUid = data['UserPage']['secUid']
    else:
        data = Api.getUserFeed(
            secUid=secUid, cursor=cursor, first=first)
        for x in data['itemList']:

            caption = str(x['desc'])
            video_id = str(x['id'])
            single_video = x
            push_db(single_video)
            all.append((video_id, genUrl(video_id)))
            print("Video <<%s>> <<%s>>" %
                  (str(video_id), str(caption)))

            count += 1
            if count == limit:
                flag = 1
                break
        if not data['hasMore']:
            break
        cursor = data['cursor']
    if flag == 1:
        break
    first = False
print(count, 'all_video')

Api.closeBrowser()


async def download_all():
    async def one(video_id, url_video):
        if not os.path.exists(f"{path}/{video_id}.mp4"):
            print(url_video)
            link = await tt_get_link(url_video)
            await download(video_id, link, path)
            print(f"{video_id} download DONE!!!")
        else:
            print(path, '/', video_id, "existed")
    coros = [one(video_id, url_video) for video_id, url_video in all]
    step = 15
    for i in range(len(coros)):
        await asyncio.gather(*coros[i*step: step*(i + 1)])

    print('ALLMUST DONE')


loop = asyncio.get_event_loop()
loop.run_until_complete(download_all())
