import time
from vk_profile import Profile
from ya_uploader import YaUploader

# скачивания информации о пользователе на ПК
start_time = time.time()
Person = Profile(input('Введите ID пользователя: '))
Person.save_photos()

# Загрузка в Яндекс диск
uploader = YaUploader()
result = uploader.upload_files(Person.path_photos)
# print(result)
print(f'Время выполнения: {time.time() - start_time}')
