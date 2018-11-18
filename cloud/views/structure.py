import hashlib
from json import dumps

from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import etag

from cloud.models import University

HIERARCHY_CACHE_TAG = "hierarchyCacheTag"


def get_etag(_request):
    return cache.get(HIERARCHY_CACHE_TAG, None)


def set_etag(tag):
    cache.set(HIERARCHY_CACHE_TAG, tag)


@etag(get_etag)
@cache_page(60 * 15)
def hierarchy_dump(request):
    response_object = {
        'universities': {
            u.id: u.as_hierarchical_dict()
            for u in University.objects.filter(is_approved=True)
        }
    }
    set_etag(json_md5(response_object))
    return JsonResponse(response_object)


def json_md5(obj):
    dump = dumps(obj).encode('utf-8')
    hash_sum = hashlib.md5()
    hash_sum.update(dump)
    md5 = hash_sum.hexdigest()
    return md5
