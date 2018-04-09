from django.shortcuts import render

from cloud.vkontakte import fetch_and_sort_memes_from_all_groups


def get_memes(request):
    memes = fetch_and_sort_memes_from_all_groups()
    return render(request, "memes.html", {"memes": memes})
