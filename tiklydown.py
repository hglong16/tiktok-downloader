import asyncio
import sqlite3
import sys

import aiofiles
import aiohttp


def append_db(data):
    con = sqlite3.connect("../tiktok.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO tiktok VALUES (?)", data)


url = "https://www.tiktok.com/@thaovy1590/video/7164747239729024282?is_from_webapp=1&sender_device=pc&web_id=7169447631952266758"
tiklydown = "https://developers.tiklydown.me/api/download?url="


async def main():
    async with aiohttp.ClientSession() as session:
        metadata = False
        async with session.get(tiklydown + url) as response:
            metadata = await response.json()
            print(metadata)
            print(metadata["video"]["noWatermark"])

        if metadata:
            async with session.get(metadata["video"]["noWatermark"]) as res:
                f = await aiofiles.open(f"download/{metadata['id']}.mp4", mode="wb")
                await f.write(await res.read())
                await f.close()
                for key in metadata.keys():
                    print(f"{key}: {metadata[key]}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
