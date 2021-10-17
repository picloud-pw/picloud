import vk
import time
import re

from vk.exceptions import VkAPIError

from PiCloud.settings.common import VK_GLOBAL_TOKEN, VK_GROUP_TOKEN, VK_API_VERSION


def fetch_memes_for_group(group_uri: str) -> list:
    session = vk.Session(access_token=VK_GLOBAL_TOKEN)
    vk_api = vk.API(session)
    kwargs = {
        'count': 10,
        'v': VK_API_VERSION
    }
    match = re.match('^club(\d)+$', group_uri)
    if match:
        kwargs['owner_id'] = -int(match.group(1))
    else:
        kwargs['domain'] = group_uri
    try:
        return vk_api.wall.get(**kwargs)["items"]
    except VkAPIError as e:
        return list()


def fetch_and_sort_memes(sources):
    memes = list()
    for source in sources:
        memes.extend(
            fetch_memes_for_group(source.source.split('/')[-1])
        )
    memes.sort(key=lambda post: post['date'], reverse=True)
    return memes


def bot_answer(vk_api, user_id, msg):
    if msg is not None:
        vk_api.messages.send(user_id=user_id, message=msg, v=VK_API_VERSION)


def bot_logic(vk_api, user_id, msg):
    words = msg.lower().split(" ")
    bot_answer(vk_api=vk_api, user_id=user_id, msg=words[0])


def vk_bot():
    session = vk.Session(access_token=VK_GROUP_TOKEN)
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
        time.sleep(1)
