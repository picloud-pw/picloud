from django.shortcuts import render, redirect

from cloud.vkontakte import fetch_and_sort_memes
from cloud.models import MemeSource, UserInfo

from .authentication import sign_in


def get_memes(request):
    if request.user.is_authenticated:
        sources = MemeSource.objects.all()[:10]
        user_info = UserInfo.objects.get(user=request.user)
        if user_info.program is not None:
            # TODO сделать нормальную подборку мемов по всем полям
            sources = MemeSource.objects.filter(university=user_info.program.chair.department.university)
            if not sources:
                sources = MemeSource.objects.all()[:10]
        memes = fetch_and_sort_memes(sources)
        return render(request, "memes.html", {"memes": memes, "sources": sources})
    else:
        return sign_in(request, msg="Пожалуйста, авторизуйтесь для просмотра мемесов."
                                    "Если вы укажите место учебы, "
                                    "мемы будут подбираться с учётом локальности!")
