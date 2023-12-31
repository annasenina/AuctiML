import os
from os.path import isdir
import shutil

from datetime import date
from tqdm import tqdm

import requests

from concurrent.futures import ThreadPoolExecutor
from threading import local

import json
import pandas as pd
import warnings


class APIDownload:
    """Скачивание JSON из API по указаным урлам"""

    def __init__(self, path: str = ''):
        thread_local = local()
        if not hasattr(thread_local, 'session'):
            thread_local.session = requests.Session()
        self.session = thread_local.session
        self.path = path

    def download_link(self, fname: str, url: str) -> None:
        """
        Метод Скачивает json по указанному url и сохраняет в отдельный файл
        :param fname: Название файла куда сохрнаять скачанный json
        :param url: URL для выгрузки json
        """
        with self.session.get(url) as response:
            if response.status_code == 200:
                with open(fname + ".json", "w", encoding="utf-8") as file:
                    file.write(response.text)

    def download_all(self, urls: dict, sub_path: str = 'jsons', workers: int = 5) -> None:
        """
        Метод проходит по словарю urls и скачивыает json в отдельный файл
        :param urls: словарь url-ов
        :param sub_path: путь куда сохранять json файлы
        :param workers: кол-во паллельных процессов
        """
        if not isdir(self.path + sub_path):
            os.mkdir(self.path + sub_path)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for fname in tqdm(urls):
                executor.submit(self.download_link, fname=(self.path + sub_path + "/" + fname), url=urls[fname])
                # s = executor.submit(self.download_link, fname=(self.path + sub_path + "/" + fname), url=urls[fname])
                # print(s.exception())


class TorgiGenerateURL:
    def __init__(self, path: str = ''):
        self.path = path
        self.api_download = APIDownload(path=self.path)
        self.list_objects_url = {}
        self.objects_url = {}

    def generate_url_list_objects(self, batch_size: int = 10, pages: int = 10, cat_code: int = 2) -> dict:
        """
        Список торгов представлен в виде страниц (page), доступ к которым можно получить через внутренний API
        Данная функция генерирует список URL для страниц торгов (pages), откуда следующим шагом будут получены id торгов
        :param batch_size: кол-во торгов на одной странице
        :param pages: кол-во страниц
        :param cat_code: номер категории, для земельных участков = 2
        :return: словарь {"уникальное название страницы": url страницы}
        """
        today = date.today().strftime("%Y_%m_%d")
        for page in range(pages):
            url = f"https://torgi.gov.ru/new/api/public/lotcards/search?catCode={cat_code}&byFirstVersion=true&withFacets=false&page={page}&size={batch_size}&sort=firstVersionPublicationDate,desc"
            json_name = f"{today}_batch_{batch_size}_pages_{page}_cat_{cat_code}"
            self.list_objects_url[json_name] = url
        return self.list_objects_url

    def generate_url_ad_torgi(self, ids: list) -> dict:
        """
        Генерация списка url-адресов по списку id объектов
        :param ids: Список id объявлений
        :return: словарь {"уникальное название страницы": url страницы}
        """
        today = date.today().strftime("%Y_%m_%d")
        for id_ad in ids:
            url = f"https://torgi.gov.ru/new/api/public/lotcards/{id_ad}"
            json_name = f"{today}_{id_ad}"
            self.objects_url[json_name] = url
        return self.objects_url

    def get_objects_id(self, json_path: str) -> list:
        """
        Сбор id торгов по выгруженным страницам
        :param json_path: путь к файлам json по выгруженным страницам
        :return: список id для каждого объявления по торгу
        """
        objects = []
        for fname in os.listdir(json_path):
            if fname.split('.')[-1] == "json":
                if os.path.getsize(json_path + '/' + fname) > 0:
                    with open(json_path + '/' + fname, 'r', encoding='utf-8') as fhandler:
                        page_json = json.load(fhandler)
                        for obj in page_json['content']:
                            objects.append(obj['id'])
        return objects

    def get_objects(self, json_path: str) -> pd.DataFrame:
        """
        Сбор информации по каждому выгруженному торгу
        :param json_path: путь к файлам json по торгам
        :return: pandas.DataFrame - датафрейм с данными по торгам
        """
        # Особенность Pandas, что если для какой-то колонки ранее не было значений, то когда появляется новый признак,
        # которого ранее не было для всех предыдущих данных ставится значенее NaN. Но когда появляется тип Bool pandas
        # пораждает предупреждение FutureWarning. В следующих версиях pandas данная проблема должна быть решена.
        warnings.simplefilter(action='ignore', category=FutureWarning)
        df = None
        for fname in tqdm(os.listdir(json_path)):
            if fname.split('.')[-1] == "json":
                with open(json_path + '/' + fname, 'r', encoding='utf-8') as fhandler:
                    object_json = json.load(fhandler)
                    df = pd.concat([df, pd.Series(object_json).to_frame().T])
        return df

    def get_data(self, batch_size: int = 10, pages: int = 10, cat_code: int = 2, clear_pages: bool = True,
                 clear_objects: bool = False, workers: int = 5) -> pd.DataFrame:
        """
        :param batch_size: кол-во торгов на одной странице
        :param pages: кол-во страниц
        :param cat_code: номер категории, для земельных участков = 2
        :param clear_pages: удалять ли json-файлы по страницам
        :param clear_object: удалять ли json-файлы по самим объектам
        :param workers: кол-во паллельных процессов
        :return: pandas.DataFrame - датафрейм с данными по торгам
        """

        # генерируем URL страниц списков объектов
        url_dict = self.generate_url_list_objects(batch_size=batch_size, pages=pages, cat_code=cat_code)
        print(f"Выбрано {len(url_dict)} страниц с торгами")

        # Скачиываем страницы списков объектов
        path_list_objects = self.path + 'list_obj_jsons'
        self.api_download.download_all(url_dict, sub_path=path_list_objects, workers=workers)

        # Определяем id торгов на основе скачанных json page
        objects_id = self.get_objects_id(json_path=path_list_objects)
        print(f"Выбрано {len(objects_id)} объектов")

        # генерируем URL для каждого объекта
        objects_url = self.generate_url_ad_torgi(objects_id)
        path_objects = self.path + 'torgi_json'
        self.api_download.download_all(objects_url, sub_path=path_objects, workers=workers)

        print(f'download {len(objects_url)} objects from {len(url_dict)} pages')
        # Формируем из json объектов DataFrame
        df_torgi = self.get_objects(json_path=path_objects)

        if clear_pages:
            shutil.rmtree(path_list_objects)
        if clear_objects:
            shutil.rmtree(path_objects)

        return df_torgi


if __name__ == "__main__":
    # Пример использования парсера сайта https://torgi.gov.ru/
    PATH = ''

    torgi_urls = TorgiGenerateURL(path=PATH)
    df_torgi = torgi_urls.get_data(batch_size=1000, pages=1000, cat_code=2, clear_pages=False, clear_objects=False,
                                   workers=5)

    PATH_DATASET = PATH  # + "../../../datasets/"
    if df_torgi is not None:
        df_torgi.set_index('id').to_csv(PATH_DATASET + "torgi_dataset.csv", index_label='id')
