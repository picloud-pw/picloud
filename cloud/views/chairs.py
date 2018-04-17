from django.shortcuts import render, get_object_or_404, redirect

from cloud.forms import NewChairForm
from cloud.models import Chair
from cloud.views.message import message
from cloud.views.posts import can_user_publish_instantly


def new_chair(request):
    if request.method == "POST":
        success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

        new_chair = NewChairForm(request.POST)
        if new_chair.is_valid():
            chair = new_chair.save(commit=False)
            chair.is_approved = can_user_publish_instantly(request.user)
            chair.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Кафедра" заполнено некорректно')
    else:
        new_chair = NewChairForm()
        return render(request, 'structure/new/chair.html', {'new_chair': new_chair})


def chair_delete(request, chair_id):
    chair = get_object_or_404(Chair, pk=chair_id)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        chair.delete()
    return redirect("moderation")


def chair_approve(request, chair_id):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Chair.objects.filter(pk=chair_id).update(is_approved=True)
        return redirect("moderation")
    else:
        return redirect("post_list")
