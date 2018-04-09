from django.shortcuts import render

from cloud.forms import NewChairForm
from cloud.views import NOT_VALID
from cloud.views.message import message


def new_chair(request):
    if request.method == "POST":
        success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

        new_chair = NewChairForm(request.POST)
        if new_chair.is_valid():
            chair = new_chair.save(commit=False)
            chair.validate_status = NOT_VALID
            chair.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Кафедра" заполнено некорректно')
    else:
        new_chair = NewChairForm()
        return render(request, 'structure/new/chair.html', {'new_chair': new_chair})
