import time
from vk_profile import Profile

start_time = time.time()
Person = Profile('405534986')
Person.photo_get()
print(Person.url_photos_profile)
print(f'Время выполнения: {time.time() - start_time}')
Person.download_photo()
