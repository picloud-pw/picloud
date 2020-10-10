from django.http import JsonResponse

from memes.models import MemesSource
from memes.vkontakte import fetch_and_sort_memes


def get_sources(request):
    sources = MemesSource.objects.all()

    return JsonResponse({'sources': [
        source.as_dict() for source in sources
    ]})


def get_memes(request):
    sources_ids = request.GET.get('ids', '').split(',')
    sources = MemesSource.objects.filter(id__in=sources_ids)

    memes = fetch_and_sort_memes(sources)
    return JsonResponse({
        'memes': memes
    })
