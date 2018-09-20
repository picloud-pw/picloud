from django.conf import settings
from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render

import requests
import vk
import time
import re

from django.urls import reverse

from cloud.models import UserInfo
from cloud.views.authentication import user_info_to_session

VK_API_VERSION = '5.74'
VK_ID = '6477166'
VK_SECRET = 'loqcCdT0JDj5fTrQd0ku'

GLOBAL_TOKEN = getattr(settings, 'VK_GLOBAL_TOKEN', None)
GROUP_TOKEN = getattr(settings, 'VK_GROUP_TOKEN', None)
if GLOBAL_TOKEN is None or GROUP_TOKEN is None:
    raise ImproperlyConfigured('Cannot get VK access token from application settings')

POSTS_COUNT = 10
BOT_LOOP_TIMEOUT = 1


def fetch_memes_for_group(vk_api, group_uri):
    match = re.match('^club(\d)+$', group_uri)
    if match:
        group_id = int(match.group(1))
        return vk_api.wall.get(owner_id=-group_id,
                               count=POSTS_COUNT,
                               v=VK_API_VERSION)["items"]
    else:
        return vk_api.wall.get(domain=group_uri,
                               count=POSTS_COUNT,
                               v=VK_API_VERSION)["items"]


def fetch_and_sort_memes(sources):
    session = vk.Session(access_token=GLOBAL_TOKEN)
    vk_api = vk.API(session)

    memes = [meme
             for source in sources
             for meme in fetch_memes_for_group(vk_api, source.link.split('/')[-1])]

    def sort_by_date(post):
        return post["date"]

    memes.sort(key=sort_by_date, reverse=True)
    return memes


def bot_answer(vk_api, user_id, msg):
    if msg is not None:
        vk_api.messages.send(user_id=user_id, message=msg, v=VK_API_VERSION)


def bot_logic(vk_api, user_id, msg):
    words = msg.lower().split(" ")
    bot_answer(vk_api=vk_api, user_id=user_id, msg=words[0])


def vk_bot():
    session = vk.Session(access_token=GROUP_TOKEN)
    vk_api = vk.API(session)

    # TODO: Переделать на LongPoll
    last_msg = 0
    while True:
        # при первом запуске просматривает сообщения за последние 10 сек., но может повторно ответить на прочитанные
        resp = vk_api.messages.get(last_message_id=last_msg, count=100, time_offset=10, v=VK_API_VERSION)
        if resp['items']:
            last_msg = resp['items'][0]['id']
        for msg in resp['items']:
            bot_logic(vk_api=vk_api, user_id=msg['user_id'], msg=msg['body'])
        time.sleep(BOT_LOOP_TIMEOUT)


def vk_get_auth_link(request):
    REDIRECT_URI = request.build_absolute_uri(reverse('vk_auth_callback'))

    return "https://oauth.vk.com/authorize?" + \
           "client_id=" + VK_ID + \
           "&display=page" \
           "&redirect_uri=" + REDIRECT_URI + \
           "&response_type=code" \
           "&v=" + VK_API_VERSION


def vk_auth_callback(request):
    code = request.GET["code"]

    REDIRECT_URI = request.build_absolute_uri(reverse('vk_auth_callback'))
    
    URL = 'https://oauth.vk.com/access_token?' \
          'client_id=' + VK_ID + \
          '&client_secret=' + VK_SECRET + \
          '&code=' + code + \
          '&redirect_uri=' + REDIRECT_URI

    if request.user.is_authenticated:
        if code is not None:
            data = requests.get(URL).json()
            vk_id = data['user_id']
            user_info = UserInfo.objects.get(user=request.user)
            user_info.vk_id = vk_id
            user_info.save()
            return redirect("settings")
        else:
            error = request.GET('error_description')
            return render(request, 'settings.html', {'error': error, 'host': request.get_host() })
    else:
        if code is not None:
            data = requests.get(URL).json()
            vk_id = data['user_id']
            user_info = UserInfo.objects.filter(vk_id=vk_id)
            if user_info.count():
                user = user_info.first().user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                user_info_to_session(request, user)
                return redirect("cloud")
            else:
                error = "Ваша ВК старница не привязана ни к одному пользователю PiCloud! Для начала авторизуйтесь."
                return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(), })
        else:
            error = request.GET('error_description')
            return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(), })


def del_vk_id(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=request.user)
        user_info.vk_id = None
        user_info.save()
        return redirect("settings")
    else:
        return redirect("signin")
