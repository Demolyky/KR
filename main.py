import time
from vk_profile import Profile
import settings
from ya_uploader import YaUploader

start_time = time.time()
Person = Profile('405534986')
Person.photo_get()
# print(Person.url_photos_profile)
Person.download_photo()

uploader = YaUploader()
result = uploader.upload_files('/Users/demolyky/Documents/Project/KR/Evgeniya_Daronovski')
print(result)
print(f'Время выполнения: {time.time() - start_time}')
