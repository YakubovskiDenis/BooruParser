import requests
import os
import time
import asyncio
from telegaSpam import SendAfterParse
def download_image(url, id, artist, save_dir,file_ext):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{id}-{artist}.{file_ext}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Изображение сохранено: {file_path}")
    else:
        print(f"Ошибка загрузки изображения: {response.status_code}")

EXECUTION_TIMEOUT=14400#4 часа
def GetImagesList(IPname,SaveDir):
    response2list = requests.get(f"https://danbooru.donmai.us/posts.json?tags={IPname}+english_text&limit=20&page=1").json()
    for response in response2list:
        for key, value in response.items():
            IMG_variants = response['media_asset']
            id = response['id']
            if not IMG_variants.get('variants'):
                continue
            for variant in IMG_variants['variants']:
                if variant['type'] == 'original':
                    url = variant['url']
                    fileExt = variant['file_ext']
            print(url)
            print(fileExt)
            if url == "":
                url = response['large_file_url']
                print(url)
            if response['tag_string_artist'] == "":
                artist = "1".replace('/', '')
            else:
                artist = response['tag_string_artist'].replace('/', '')
            download_image(url,id,artist,SaveDir,fileExt)
            break
 
def BooruFetch():
    DirNames=["HSR","Arknights","ZZZ","GFL","GI"]
    GetImagesList("honkai%3A_star_rail", "HSR")
    asyncio.run(SendAfterParse(DirNames[0]))
    GetImagesList("arknights","Arknights")
    asyncio.run(SendAfterParse(DirNames[1]))
    GetImagesList("zenless_zone_zero","ZZZ")
    asyncio.run(SendAfterParse(DirNames[2]))
    GetImagesList("girls%27_frontline","GFL")
    asyncio.run(SendAfterParse(DirNames[3]))
    GetImagesList("genshin_impact","GI")
    asyncio.run(SendAfterParse(DirNames[4]))

while True:
    #блок по работе с данбору
    BooruFetch()
    print("Цикл сохранения изображений пройден. Перехожу в сон.")
    time.sleep(EXECUTION_TIMEOUT)#регулирует частоту запросов на бору


#https://danbooru.donmai.us/posts.json?tags=belfast_(azur_lane)&limit=100&page=1
#https://gist.githubusercontent.com/bem13/0bc5091819f0594c53f0d96972c8b6ff/raw/b0aacd5ea4634ed4a9f320d344cc1fe81a60db5a/danbooru_tags_post_count.csv