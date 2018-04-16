from django.shortcuts import render

from cloud.forms import NewDepartmentForm
from cloud.views import NOT_VALID
from cloud.views.message import message
from cloud.views.posts import can_user_publish_instantly


def new_department(request):
    if request.method == "POST":
        success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

        new_department = NewDepartmentForm(request.POST)
        if new_department.is_valid():
            department = new_department.save(commit=False)
            department.is_approved = can_user_publish_instantly(request.user)
            department.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Факультет" заполнено некорректно')
    else:
        new_department = NewDepartmentForm()
        return render(request, 'structure/new/department.html', {'new_department': new_department})
