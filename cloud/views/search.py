import operator
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from cloud.models import Post, University, Department, Chair, Program, Subject
from .posts import POSTS_PER_PAGE


def text_search(request):
    text_request = request.GET.get('request', None)
    if text_request is not None:
        words = text_request.split(" ")

        posts = Post.objects.filter(is_approved=True)
        posts = posts.filter(reduce(operator.or_, (Q(title__icontains=x) for x in words)))
        posts = posts.order_by('created_date').reverse()[:100]
        posts = [p.title for p in posts]

        universities = University.objects.filter(is_approved=True)
        universities = universities.filter(
            reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
        )
        universities = [u.title for u in universities]

        departments = Department.objects.filter(is_approved=True)
        departments = departments.filter(
            reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
        )
        departments = [d.title for d in departments]

        chairs = Chair.objects.filter(is_approved=True)
        chairs = chairs.filter(
            reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
        )
        chairs = [c.title for c in chairs]

        programs = Program.objects.filter(is_approved=True)
        programs = programs.filter(
            reduce(operator.or_, (Q(code__icontains=x) | Q(title__icontains=x) for x in words))
        )
        programs = [d.title for d in programs]

        subjects = Subject.objects.filter(is_approved=True)
        subjects = subjects.filter(
            reduce(operator.or_, (Q(short_title__icontains=x) | Q(title__icontains=x) for x in words))
        )
        subjects = [d.title for d in subjects]

        request = {
            "posts": posts,
            "universities": universities,
            "departments": departments,
            "chairs": chairs,
            "programs": programs,
            "subjects": subjects
        }
        return JsonResponse(request, safe=False)
    else:
        return JsonResponse([], safe=False)


def search_posts(request):
    words = request.GET.get('search_request', None).lover().split(" ")
    posts = Post.objects.filter(is_approved=True).filter(parent_post=None)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_and_render_posts(request):
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    page_number = request.GET.get('page', 1)
    sort_type = request.GET.get('sort_type', '0')

    posts = Post.objects.filter(is_approved=True).filter(parent_post=None)

    if subject_id is None and type_id is None:
        if request.user.is_authenticated:
            user_info = request.user.userinfo
            if user_info.program is not None:
                posts = posts.filter(subject__programs__exact=user_info.program.pk)

    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)

    if '0' == sort_type:
        posts = posts.order_by('created_date').reverse()
    if '1' == sort_type:
        posts = posts.order_by('created_date')
    if '2' == sort_type:
        posts = posts.order_by('subject__semester').reverse()
    if '3' == sort_type:
        posts = posts.order_by('subject__semester')
    if '4' == sort_type:
        posts = posts.order_by('views').reverse()
    if '5' == sort_type:
        posts = posts.order_by('views')

    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page_number)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = []

    return JsonResponse({
        'current_page': posts_page.number,
        'total_pages': paginator.num_pages,
        'has_next': posts_page.has_next(),
        'html': render_to_string('cloud/bare_post_list.html', {'posts': posts_page}, request=request),
    })
