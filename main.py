import time
from vk_profile import Profile
from ya_uploader import YaUploader


def main():
    # скачивания информации о пользователе на ПК
    start_time = time.time()
    person = Profile(input('Введите ID пользователя: '))
    person.save_photos()

    # Загрузка в Яндекс диск
    uploader = YaUploader()
    result = uploader.upload_files(person.path_photos)
    # print(result)
    print(f'Время выполнения: {time.time() - start_time}')


if __name__ == '__main__':
    main()
