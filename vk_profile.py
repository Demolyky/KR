import requests
import settings
import json
import os
from threading import Thread
import sys
import time


class Profile:
    # класс работы с ВК
    def __init__(self, user_id=settings.ID_VK):
        self.access_token = settings.TOKEN_VK  # Токен для авторизации
        self.user_id = user_id  # ID пользователя
        profile_info = self.user_get(self.user_id)  # получение информации о профиле
        self.first_name = profile_info['response'][0]['first_name']  # определение имени пользователя
        self.last_name = profile_info['response'][0]['last_name']  # определение фамилии пользователя
        self.url_photos_profile = {}  # перечень лайков и url с фото в формате {'0': 'https://'}
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
        self.__error_detected(response)
        Thread(target=self.save_json, args=(response, 'userinfo',)).start()
        return response.json()

    def save_photos(
        self, user_id=settings.ID_VK, *, access_token=settings.TOKEN_VK,
        album_id='profile', extended='1', version='5.131'
    ):
        # загрузка фотографий альбома аватарок пользователя
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.access_token if access_token else access_token,
            'v': version,
            'owner_id': self.user_id if user_id else user_id,
            'album_id': album_id,
            'extended': extended
        }
        response = requests.get(url, params={**params})
        self.__error_detected(response)
        self.url_photos_profile = self.__search_photos_and_likes(response)
        Thread(target=self.save_json, args=(response, 'photos',)).start()
        self.download_photo()
        return response

    def save_json(self, response, file_name):
        # сохранение запросов в json файл корневой папки
        information = response.json()
        path = self.create_folder('profile_info')
        with open(f'{path}/{file_name}.json', "w+") as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

    def __search_photos_and_likes(self, response):
        # поиск фотографии максимального разрешения из запроса
        photos_info = response.json()
        url_photos_profile = {}
        for photos in photos_info['response']['items']:
            url = self.__search_high_resolution(photos)
            file_name = self.__verify_name_file(str(photos['likes']['count']), list(url_photos_profile.keys()))
            url_photos_profile[file_name] = url
        return url_photos_profile

    def download_photo(self):
        # запрос на скачивание фото по ссылке
        empty_photos = 0
        for likes, url in self.url_photos_profile.items():
            if url:
                response = requests.get(url)
                with open(f'{self.path_photos}/{likes}.jpg', 'wb') as img:
                    img.write(response.content)
            else:
                empty_photos += 1
        if empty_photos > 0:
            with open('empty_photos.txt', 'w+') as file_txt:
                file_txt.write(f'Фотографий не скачано из-за отсутствия ссылки: {empty_photos}')

    def __str__(self):
        return f'id: {self.user_id} Name: {self.first_name}, Family: {self.last_name}'    @staticmethod

    def __verify_name_file(self, name, list_names, number=0):
        # проверка на наличие файлов с одинаковым количеством лайков
        test_name = name + f'_{number}' if number > 0 else name
        if test_name in list_names:
            number += 1
            file_name = self.__verify_name_file(name, list_names, number)
        else:
            file_name = test_name
        return file_name

    @staticmethod
    def create_folder(folder_name):
        # создание папки для сохранения фото
        path = os.getcwd() + f'/{folder_name}'
        try:
            os.mkdir(path)
            return path
        except FileExistsError:
            return path

    @staticmethod
    def __error_detected(response):
        # проверка запроса на ошибки
        if not response.status_code == 200:
            print(f'Ошибка запроса к ВК № {response.status_code}')
            sys.exit()
        elif 'error' in response.json().keys():
            print(f'error: {response.json()["error"]["error_msg"]}')
            sys.exit()

    @staticmethod
    def __search_high_resolution(photos):
        url = ''
        index = 0
        type_index = {}
        types = ['w', 'z', 'y', 'x', 'm', 's', 'p', 'q', 'r', 'o']
        for photo in photos['sizes']:
            type_index[photo['type']] = index
            index += 1
        for t in types:
            if t in type_index:
                url = photos['sizes'][type_index[t]]['url']
                break
        return url

