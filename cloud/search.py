import operator
from functools import reduce

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

from cloud.models import Post, University, Department, Chair, Program, Subject, UserInfo
from posts.views.posts import POSTS_PER_PAGE


def text_search(request):
    text_request = request.GET.get('request', None)
    if text_request is None:
        return JsonResponse([], safe=False)
    text_request = " ".join(text_request.split())  # удаление дублирующихся пробелов
    text_request = text_request.strip()
    if not text_request:
        return JsonResponse([], safe=False)

    response = {
        "results": {}
    }
    words = text_request.split()

    posts = Post.objects.filter(is_approved=True)
    posts = posts.filter(reduce(operator.or_, (Q(title__icontains=x) for x in words)))
    posts = posts.order_by('created_date').reverse()[:10]
    posts = [{
        "title": p.title,
        "description": p.subject.programs.first().chair.department.university.short_title + " • " + p.subject.title,
        "url": reverse("post_detail", kwargs={'pk': p.pk})
    } for p in posts]
    if len(posts):
        response["results"]["Posts"] = {"name": "Посты", "results": posts}

    universities = University.objects.filter(is_approved=True)
    universities = universities.filter(
        reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
    )
    universities = [{
        "title": u.title,
        "description": u.link,
        "image": u.logo.url,
        "url": reverse("university_page", kwargs={'university_id': u.pk})
    } for u in universities]
    if len(universities):
        response["results"]["University"] = {"name": "Университеты", "results": universities}

    departments = Department.objects.filter(is_approved=True)
    departments = departments.filter(
        reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
    )
    departments = [{
        "title": d.title,
        "description": d.university.short_title,
        "url": reverse("university_page", kwargs={'university_id': d.pk})
    } for d in departments]
    if len(departments):
        response["results"]["Department"] = {"name": "Факультеты", "results": departments}

    chairs = Chair.objects.filter(is_approved=True)
    chairs = chairs.filter(
        reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
    )
    chairs = [{
        "title": c.title,
        "description": c.department.university.short_title + " • " + c.department.short_title,
        "url": reverse("university_page", kwargs={'university_id': c.pk})
    } for c in chairs]
    if len(chairs):
        response["results"]["Chair"] = {"name": "Кафедры", "results": chairs}

    programs = Program.objects.filter(is_approved=True)
    programs = programs.filter(
        reduce(operator.or_, (Q(code__icontains=x) | Q(title__icontains=x) for x in words))
    )
    programs = [{
        "title": d.title,
        "description": d.chair.department.university.short_title + " • " + d.chair.short_title,
        "url": reverse("program_page", kwargs={'program_id': d.pk})
    } for d in programs]
    if len(programs):
        response["results"]["Program"] = {"name": "Программы обучения", "results": programs}

    subjects = Subject.objects.filter(is_approved=True)
    subjects = subjects.filter(
        reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
    )
    subjects = [{
        "title": str(d.title) + " (сем. " + str(d.semester) + ")",
        "description": str(d.programs.first().chair.department.university.short_title),
        "url": reverse("subject_page", kwargs={'subject_id': d.pk})
    } for d in subjects]
    if len(subjects):
        response["results"]["Subject"] = {"name": "Предметы", "results": subjects}

    return JsonResponse(response, safe=False)