from django.shortcuts import render, redirect, get_object_or_404

from cloud.forms import NewDepartmentForm
from cloud.models import Department
from cloud.views.message import message
from posts.views.posts import can_user_publish_instantly


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


def department_delete(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        department.delete()
    return redirect("moderation")


def department_approve(request, department_id):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Department.objects.filter(pk=department_id).update(is_approved=True)
        return redirect("moderation")
    else:
        return redirect("cloud")
