from django.shortcuts import render

from cloud.vkontakte import fetch_and_sort_memes
from cloud.models import MemeSource


def get_memes(request):
    sources = MemeSource.objects.all()
    memes = fetch_and_sort_memes(sources)
    return render(request, "memes.html", {"memes": memes})
