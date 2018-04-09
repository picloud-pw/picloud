from django.shortcuts import render, get_object_or_404

from cloud.forms import NewUniversityForm
from cloud.models import University, Program, Chair, Department, Post, UserInfo
from cloud.views import VALID, NOT_VALID
from cloud.views.message import message


def universities_list(request):
    univer_list = University.objects.filter(validate_status=VALID)
    return render(request, 'structure/universities.html', {"univer_list": univer_list})


def university_page(request, university_id):
    university = get_object_or_404(University, pk=university_id)
    programs = Program.objects.filter(chair__department__university_id=university_id).filter(validate_status=VALID)
    chairs = Chair.objects.filter(program__in=programs).distinct().filter(validate_status=VALID)
    departments = Department.objects.filter(chair__in=chairs).distinct().filter(validate_status=VALID)

    posts_queryset = Post.objects.filter(subject__programs__in=programs).distinct()
    posts = posts_queryset.count()
    views = 0
    for post in posts_queryset:
        views += post.views
    persons = UserInfo.objects.filter(program__in=programs).count()

    return render(request, "structure/university_page.html", {
        "univer": university,
        "departments": departments,
        "chairs": chairs,
        "programs": programs,
        "stats": {
            "posts": posts,
            "views": views,
            "persons": persons
        }
    })


def new_university(request):
    if request.method == "POST":
        success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

        new_university = NewUniversityForm(request.POST)
        if new_university.is_valid():
            university = new_university.save(commit=False)
            university.validate_status = NOT_VALID
            university.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Университет" заполнено некорректно')
    else:
        new_university = NewUniversityForm()
        return render(request, 'structure/new/university.html', {'new_university': new_university})
