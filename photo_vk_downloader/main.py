import time
from vk_profile import Profile
from ya_uploader import YaUploader


def main():
    start_time = time.time()
    id_vk = input('Введите ID пользователя: ')
    count = input('Число фотографий: ')

    if id_vk.isdigit() and count.isdigit():
        # скачивания информации о пользователе на ПК
        person = Profile(id_vk)
        person.save_photos(count=count if count else '5')

        # Загрузка в Яндекс диск
        uploader = YaUploader()
        result = uploader.upload_files(person.path_photos)
        # print(result)
        print(f'Время выполнения: {time.time() - start_time}')
    else:
        print('Введите ЧИСЛО!')
        main()


if __name__ == '__main__':
    main()
