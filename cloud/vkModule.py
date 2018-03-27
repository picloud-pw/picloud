from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import vk
import time

VK_API_VERSION = 5.73

GLOBAL_TOKEN = getattr(settings, 'VK_GLOBAL_TOKEN', None)
GROUP_TOKEN = getattr(settings, 'VK_GROUP_TOKEN', None)
if GLOBAL_TOKEN is None or GROUP_TOKEN is None:
    raise ImproperlyConfigured('Cannot get VK access token from application settings')

VK_GROUPS = {
    'pashasmeme',
    'dnische1',
    'klimenkovdefacto',
    'itmoquotepad',
    'wisemrduck',

}
BOT_TIME_SLEEP = 1

COL_POSTS = 1000


def memes():
    session = vk.Session(access_token=GLOBAL_TOKEN)
    vk_api = vk.API(session)

    mem_posts = []
    for group_domain in VK_GROUPS:
        mem_posts.extend(
            vk_api.wall.get(domain=group_domain, count=COL_POSTS, v=VK_API_VERSION)["items"]
        )

    def sort_by_date(post):
        return post["date"]

    mem_posts.sort(key=sort_by_date, reverse=True)

    return mem_posts


def bot_answ(vk_api, user_id, msg):
    if msg is not None:
        vk_api.messages.send(user_id=user_id, message=msg, v=VK_API_VERSION)


def bot_logic(vk_api, user_id, msg):
    words = msg.lower().split(" ")
    bot_answ(vk_api=vk_api, user_id=user_id, msg=words[0])


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
        time.sleep(BOT_TIME_SLEEP)
