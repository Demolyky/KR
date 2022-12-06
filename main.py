import requests
import settings
import json


class Profile:

    def __init__(self, user_id=settings.ID_VK):
        self.access_token = settings.TOKEN_VK
        self.user_id = user_id
        profile_info = self.user_get(self.user_id).json()
        self.first_name = profile_info['response'][0]['first_name']
        self.last_name = profile_info['response'][0]['last_name']
        self.url_photos_profile = []

    def user_get(self, user_id, *, access_token=settings.TOKEN_VK, version='5.131'):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.access_token if access_token else access_token,
            'user_ids': self.user_id if user_id else user_id,
            'v': version
        }
        response = requests.get(url, params={**params})
        self.save_json(response, 'userinfo')
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
        self.search_photos_and_likes(response)
        self.save_json(response, 'photos')
        return response

    def save_json(self, response, file_name):
        information = response.json()
        with open(f'{file_name}.json', "w+") as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

    def search_photos_and_likes(self, response):
        photos_info = response.json()
        url = ''
        width_photo = 0
        for photos in photos_info['response']['items']:
            for photo in photos['sizes']:
                if width_photo < photo['width']:
                    width_photo = photo['width']
                    url = photo['url']
            self.url_photos_profile.append({photos['likes']['count']: url})
        return self.url_photos_profile

    def __str__(self):
        return f'id: {self.user_id} Name: {Person.first_name}, Family: {Person.last_name}'


Person = Profile(1)
Person.photo_get()
print(Person.url_photos_profile)






