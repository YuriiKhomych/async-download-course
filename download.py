import requests
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


def get_link_and_name_data(coursehunters_link):
    request = requests.get(coursehunters_link)
    soup = BeautifulSoup(request.content, "html.parser")
    lessons_list = soup.find_all('ul', class_='lessons-list')
    return [
        (
            link.text,
            link.findChildren("link", attrs={'itemprop': 'contentUrl'}, href=True)[0]['href']
        )
        for link in lessons_list
    ]


async def download_videos(name, link, session):
    async with session.get(link) as response:
        file_name = name.replace('\n', '')
        print(f"start getting video: {file_name} from: {link}")
        response = await response.read()
        await write_to_file(file_name, link, response)


async def write_to_file(file_name, link, response):
    async with aiofiles.open(f"{file_name}.mp4", mode='wb') as out_file:
        print(f"start writing video {file_name} from: {link}")
        await out_file.write(response)
        print(f"CONGRATULATIONS!! Done video {file_name} from: {link}")


async def asynchonous(coursehunters_link):
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_videos(name, link, session)
            for name, link in get_link_and_name_data(coursehunters_link)
        ]
        await asyncio.wait(tasks)

ioloop = asyncio.get_event_loop()
print("Paste coursehunters link with course: ")
coursehunters_link = input()
ioloop.run_until_complete(asynchonous(coursehunters_link))
ioloop.close()
