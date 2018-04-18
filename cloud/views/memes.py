from django.shortcuts import render

from cloud.vkontakte import fetch_and_sort_memes
from cloud.models import MemeSource, UserInfo


def get_memes(request):
    sources = MemeSource.objects.all()[:10]
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=request.user)
        if user_info.program is not None:
            # TODO сделать нормальную подборку мемов по всем полям
            sources = MemeSource.objects.filter(university=user_info.program.chair.department.university)
            if not sources:
                sources = MemeSource.objects.all()[:10]
    memes = fetch_and_sort_memes(sources)
    return render(request, "memes.html", {"memes": memes, "sources": sources})
