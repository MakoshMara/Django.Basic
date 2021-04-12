import os
import urllib.request
from datetime import datetime, timezone
from urllib.request import urlretrieve

import requests
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max&access_token={response['access_token']}&v=5.92"

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    print(data)
    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = datetime.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_max']:
        photo = requests.get(data['photo_max'])
        with open(os.path.join(settings.BASE_DIR, f'media/users_avatars/{user.username}.jpg'), "wb") as av:
            av.write(photo.content)
        user.avatar = f'users_avatars/{user.username}.jpg'
    user.save()
