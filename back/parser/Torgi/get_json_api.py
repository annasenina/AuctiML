import os
from datetime import date

from tqdm import tqdm

import requests
from requests.sessions import Session
import time
from threading import local
from os.path import isdir

thread_local = local()


def generateURLs(batch_size: int = 10, pages: int = 10, cat_code: int = 2) -> dict:
    urls = {}
    today = date.today().strftime("%Y_%m_%d")
    for page in range(pages):
        url = f"https://torgi.gov.ru/new/api/public/lotcards/search?catCode={cat_code}&byFirstVersion=true&withFacets=false&page={page}&size={batch_size}&sort=firstVersionPublicationDate,desc"
        json_name = f"{today}_batch_{batch_size}_pages_{page}_cat_{cat_code}"
        urls[json_name] = url
    return urls


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def download_link(fname: str, url: str):
    session = get_session()
    with session.get(url) as response:
        if response.status_code == 200:
            with open("jsons/" + fname + ".json", "w", encoding="utf-8") as file:
                file.write(response.text)


def download_all(urls: dict) -> None:
    if not isdir("jsons"):
        os.mkdir("jsons")
    for fname in tqdm(urls):
        download_link(fname=fname, url=urls[fname])


if __name__ == "__main__":
    url_dict = generateURLs(batch_size=100, pages=10, cat_code=2)
    start = time.time()
    download_all(url_dict)
    end = time.time()
    print(f'download {len(url_dict)} links in {end - start} seconds')
