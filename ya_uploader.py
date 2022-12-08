import os

import settings
import requests
from threading import Thread


def detection_last_name_in_path(file_path: str):
    return file_path.split(sep='/')[-1]

def detection_path(file_path: str):
    path_list = file_path.split(sep='/')[:-1]
    path = '/'.join(path_list)
    return path


class YaUploader:

    HOST = 'https://cloud-api.yandex.net:443'

    def __init__(self):
        self.token = settings.TOKEN_YA

    def upload_files(self, path_folder):
        path_folders = [_ for _ in os.walk(path_folder)]
        main_path = detection_path(path_folder)
        for path in path_folders:
            ya_path = path[0].replace(main_path, '')
            self.create_folder(path[0], ya_path)
            if path[2]:
                for file in path[2]:
                    Thread(target=self.upload_file, args=(path[0]+'/'+file, ya_path+'/'+file,)).start()

    def create_folder(self, path_folder, ya_path=''):
        url = self.HOST + '/v1/disk/resources/'
        params = {'path': ya_path}
        response = requests.put(url, headers=self._get_headers(), params=params)
        if 'error' in response.json().keys():
            print(response.json()['message'])
        return f'Папка {detection_last_name_in_path(path_folder)} создана'

    def upload_file(self, file_path, ya_path):
        upload_url = self._get_link_url_upload(ya_path)
        response = requests.put(upload_url, data=open(file_path, 'rb'), headers=self._get_headers())
        return response

    def _get_link_url_upload(self, file_path):
        url = '/v1/disk/resources/upload/'
        requests_url = self.HOST + url
        params = {'path': file_path, 'overwrite': True}
        response = requests.get(requests_url, headers=self._get_headers(), params=params)
        print(response.json())
        return response.json()['href']

    def _get_headers(self):
        return {
            'Content-Type': 'application.json',
            'Authorization': f'OAuth {self.token}'
            }