import requests
import settings
import json
import os
from threading import Thread


class Profile:

    def __init__(self, user_id=settings.ID_VK):
        self.access_token = settings.TOKEN_VK
        self.user_id = user_id
        profile_info = self.user_get(self.user_id).json()
        self.first_name = profile_info['response'][0]['first_name']
        self.last_name = profile_info['response'][0]['last_name']
        self.url_photos_profile = []
        self.path_photos = ''

    def user_get(self, user_id, *, access_token=settings.TOKEN_VK, version='5.131'):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.access_token if access_token else access_token,
            'user_ids': self.user_id if user_id else user_id,
            'v': version
        }
        response = requests.get(url, params={**params})
        Thread(target=self.__save_json, args=(response, 'userinfo',)).start()
        return response

    def photo_get(
            self, user_id=settings.ID_VK, *, access_token=settings.TOKEN_VK,
            album_id='profile', extended='1', count='9', version='5.131'
    ):
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
        self.url_photos_profile = list(self.__search_photos_and_likes(response))
        Thread(target=self.__save_json, args=(response, 'photos',)).start()
        return response

    def __save_json(self, response, file_name):
        information = response.json()
        path = self.create_folder('profile_info')
        with open(f'{path}/{file_name}.json', "w+") as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

    def __search_photos_and_likes(self, response):
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
        for info_photos in self.url_photos_profile:
            for likes, url in info_photos.items():
                response = requests.get(url)
                self.path_photos = self.create_folder(f'{self.first_name}_{self.last_name}')
                with open(f'{self.path_photos}/{likes}.jpg', 'wb') as img:
                    img.write(response.content)

    def create_folder(self, folder_name):
        path = os.getcwd()+f'/{folder_name}'
        try:
            os.mkdir(path)
            return path
        except FileExistsError:
            return path

    def __str__(self):
        return f'id: {self.user_id} Name: {self.first_name}, Family: {self.last_name}'