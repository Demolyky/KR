import requests
import settings
import json
import os
from threading import Thread
import sys


class Profile:
    # класс работы с ВК
    def __init__(self, user_id=settings.ID_VK):
        self.access_token = settings.TOKEN_VK  # Токен для авторизации
        self.user_id = user_id  # ID пользователя
        profile_info = self.user_get(self.user_id)  # получение информации о профиле
        self.first_name = profile_info['response'][0]['first_name']  # определение имени пользователя
        self.last_name = profile_info['response'][0]['last_name']  # определение фамилии пользователя
        self.url_photos_profile = []  # перечень лайков и url с фото в формате {'0': 'https://'}
        self.path_photos = self.create_folder(f'{self.first_name}_{self.last_name}')  # путь к папке с фото

    def user_get(self, user_id, *, access_token=settings.TOKEN_VK, version='5.131'):
        # запрос информации о пользователе
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.access_token if access_token else access_token,
            'user_ids': self.user_id if user_id else user_id,
            'v': version
        }
        response = requests.get(url, params={**params})
        self.error_detected(response)
        Thread(target=self.__save_json, args=(response, 'userinfo',)).start()
        return response.json()

    def save_photos(
        self, user_id=settings.ID_VK, *, access_token=settings.TOKEN_VK,
        album_id='profile', extended='1', count='9', version='5.131'
    ):
        # загрузка фотографий альбома аватарок пользователя
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.access_token if access_token else access_token,
            'v': version,
            'owner_id': self.user_id if user_id else user_id,
            'album_id': album_id,
            'extended': extended,
            'count': count
        }
        response = requests.get(url, params={**params})
        self.error_detected(response)
        self.url_photos_profile = list(self.__search_photos_and_likes(response))
        Thread(target=self.__save_json, args=(response, 'photos',)).start()
        self.download_photo()
        return response


    def __save_json(self, response, file_name):
        # сохранение запросов в json файл корневой папки
        information = response.json()
        path = self.create_folder('profile_info')
        with open(f'{path}/{file_name}.json', "w+") as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

    def __search_photos_and_likes(self, response):
        # поиск фотографии максимального разрешения из запроса
        photos_info = response.json()
        url = ''
        for photos in photos_info['response']['items']:
            width_photo = 0
            for photo in photos['sizes']:
                if width_photo < photo['width']:
                    width_photo = photo['width']
                    url = photo['url']
            yield {photos['likes']['count']: url}

    def download_photo(self):
        # запрос на скачивание фото по ссылке
        for info_photos in self.url_photos_profile:
            for likes, url in info_photos.items():
                response = requests.get(url)
                with open(f'{self.path_photos}/{likes}.jpg', 'wb') as img:
                    img.write(response.content)

    def create_folder(self, folder_name):
        # создание папки для сохранения фото
        path = os.getcwd() + f'/{folder_name}'
        try:
            os.mkdir(path)
            return path
        except FileExistsError:
            return path

    def __str__(self):
        return f'id: {self.user_id} Name: {self.first_name}, Family: {self.last_name}'

    def error_detected(self, response):
        # проверка запроса на ошибки
        if not response.status_code == 200:
            print(f'Ошибка запроса к ВК № {response.status_code}')
            sys.exit()
        elif 'error' in response.json().keys():
            print(f'error: {response.json()["error"]["error_msg"]}')
            sys.exit()

