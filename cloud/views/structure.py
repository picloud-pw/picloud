import hashlib
import json

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import etag

from cloud.models import University

HIERARCHY_CACHE_TAG = "hierarchyCacheTag"


def get_etag(_request):
    return cache.get(HIERARCHY_CACHE_TAG, None)


def set_etag(tag):
    cache.set(HIERARCHY_CACHE_TAG, tag)


@etag(get_etag)
@cache_page(24 * 60 * 60)
def hierarchy_dump(request):
    obj = {
        'universities': {
            u.id: u.as_hierarchical_dict()
            for u in University.objects.filter(is_approved=True)
        }
    }
    dump = json.dumps(obj, sort_keys=True).encode('utf-8')
    set_etag(md5(dump))
    return HttpResponse(dump, content_type="application/json")


def md5(data):
    hash_sum = hashlib.md5()
    hash_sum.update(data)
    md5 = hash_sum.hexdigest()
    return md5
