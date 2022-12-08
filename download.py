import asyncio
import os
import sys
import time

from TiktokApi import *
from ttdownloader import download, tt_get_link

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def main():
    username = input("Tiktoker's id  exp: khaby00 for Khaby Lame \n:@")
    limit = input("How many video you want download, default = 30: ")

    Api = Tiktok()

    # edit username  here
    if username == "":
        print("fail")
        return None

    if not os.path.exists(f"./download/{username}"):
        os.makedirs(f"./download/{username}")
    path = f"./download/{username}"
    url = "https://tiktok.com/@%s" % username

    def genUrl(id):
        return f"https://tiktok.com/@{username}/video/{id}"

    Api.openBrowser(url, True)
    input("Skip the captcha, press Enter to continue ")
    limit = 10000 if limit == "" else int(limit)
    count = 0
    first = True
    flag = 0
    cursor = 0
    secUid = ""
    all = []
    while True:

        if first == True:
            data = Api.getUserFeed(first=first)
            for x in data["ItemModule"]:

                video_id = data["ItemModule"][x]["id"]
                caption = data["ItemModule"][x]["desc"]
                single_video = data["ItemModule"][x]
                all.append((video_id, genUrl(video_id)))
                print("Video <<%s>> <<%s>>" % (str(video_id), str(caption)))

                count += 1
                if count == limit:
                    flag = 1
                    break
            if not data["ItemList"]["user-post"]["hasMore"]:
                break
            cursor = data["ItemList"]["user-post"]["cursor"]
            secUid = data["UserPage"]["secUid"]
        else:
            data = Api.getUserFeed(secUid=secUid, cursor=cursor, first=first)
            for x in data["itemList"]:

                caption = str(x["desc"])
                video_id = str(x["id"])
                single_video = x
                all.append((video_id, genUrl(video_id)))
                print("Video <<%s>> <<%s>>" % (str(video_id), str(caption)))

                count += 1
                if count == limit:
                    flag = 1
                    break
            if not data["hasMore"]:
                break
            cursor = data["cursor"]
        if flag == 1:
            break
        first = False
    print(count, "all_video")

    Api.closeBrowser()

    async def download_all():
        async def one(video_id, url_video):
            if not os.path.exists(f"{path}/{video_id}.mp4"):
                print(url_video)
                link = await tt_get_link(url_video)
                await download(video_id, link, path)
                print(f"{video_id} download DONE!!!")
            else:
                print(path, "/", video_id, "existed")

        coros = [one(video_id, url_video) for video_id, url_video in all]
        step = 15
        for i in range(len(coros)):
            await asyncio.gather(*coros[i * step : step * (i + 1)])

        print("ALLMUST DONE")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_all())


if __name__ == "__main__":
    main()
