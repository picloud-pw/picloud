from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import vk
import json

VK_API_VERSION = 5.73

ACCESS_TOKEN = getattr(settings, 'VK_GLOBAL_TOKEN', None)
if ACCESS_TOKEN is None:
    raise ImproperlyConfigured('Cannot get VK access token from application settings')

VK_GROUPS = {
    'pashasmeme',
}

COL_POSTS = 1000


def memes():
    session = vk.Session(access_token=ACCESS_TOKEN)
    vk_api = vk.API(session)

    mem_posts = []
    for group_domain in VK_GROUPS:
        mem_posts.extend(
            vk_api.wall.get(domain=group_domain, count=COL_POSTS, v=VK_API_VERSION)["items"]
        )

    return mem_posts
