import requests
import os
import asyncio
from telegaSpam import SendAfterParse
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 10  # количество параллельных потоков

def download_image(url, id, artist, save_dir, file_ext):
    try:
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"{id}-{artist}.{file_ext}")
        if os.path.exists(file_path):
            print(f"Файл уже есть: {file_path}")
            return
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Сохранено: {file_path}")
        else:
            print(f"Ошибка загрузки: {response.status_code} | URL: {url}")
    except Exception as e:
        print(f"Ошибка: {e}")


def downloadallfromsingletag(Tagname: str):
    page = 1
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            print(f"Загрузка страницы {page}")
            try:
                response = requests.get(
                    f"https://danbooru.donmai.us/posts.json?tags={Tagname}&limit=100&page={page}",
                    timeout=10
                )
                response.raise_for_status()
                response2list = response.json()
            except Exception as e:
                print(f"Ошибка получения данных: {e}")
                break

            if not response2list:
                print("Больше нет постов.")
                break

            futures = []
            for post in response2list:
                try:
                    id = post['id']
                    fileExt = post.get('file_ext', 'jpg')
                    artist = post.get('tag_string_artist', 'unknown').replace('/', '_') or "unknown"
                    url = None

                    # получаем оригинал
                    variants = post.get('media_asset', {}).get('variants', [])
                    for variant in variants:
                        if variant.get('type') == 'original':
                            url = variant.get('url')
                            break

                    if not url:
                        url = post.get('large_file_url')

                    if url:
                        futures.append(
                            executor.submit(download_image, url, id, artist, Tagname, fileExt)
                        )
                except Exception as e:
                    print(f"Ошибка обработки поста: {e}")
                    continue

            # Ожидание завершения всех задач на текущей странице
            for future in as_completed(futures):
                future.result()

            page += 1


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
            if url == "":
                url = response['large_file_url']
                print(url)
            if response['tag_string_artist'] == "":
                artist = "1".replace('/', '')
            else:
                artist = response['tag_string_artist'].replace('/', '')
            download_image(url,id,artist,SaveDir,fileExt)
            break

def GetCountOfWorksByTag(Tag: str):
    count = 0
    page = 0
    while True:
        response2list = requests.get(f"https://danbooru.donmai.us/posts.json?tags={Tag}&limit=1000&page={page}").json()
        page+=1
        for response in response2list:
            print(response['id'], "\n")
            count+=1
            print(f"Текущее количество найденных работ по тегу: {count}")
            if response['id'] == None:
                break

def GetLinksTranslated(IPname):
    response2list = requests.get(f"https://danbooru.donmai.us/posts.json?tags={IPname}+translated&limit=20&page=1").json()
    for response in response2list:
        for key, value in response.items():
            print(key, value)

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
    

downloadallfromsingletag("maiqo")

#while True:
    #блок по работе с данбору
    #BooruFetch()
    #GetCountOfWorksByTag("Arknights")
    #print("Цикл сохранения изображений пройден. Перехожу в сон.")
    #time.sleep(EXECUTION_TIMEOUT)#регулирует частоту запросов на бору


#https://danbooru.donmai.us/posts.json?tags=belfast_(azur_lane)&limit=100&page=1
#https://gist.githubusercontent.com/bem13/0bc5091819f0594c53f0d96972c8b6ff/raw/b0aacd5ea4634ed4a9f320d344cc1fe81a60db5a/danbooru_tags_post_count.csv