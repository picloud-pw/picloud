from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone

from cloud.models import Post
from .posts import POSTS_PER_PAGE


def search_posts(request):
    words = request.GET.get('search_request', None).lover().split(" ")
    posts = Post.objects.filter(is_approved=True)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_and_render_posts(request):
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    page_number = request.GET.get('page', 1)

    posts = Post.objects.filter(is_approved=True)

    if subject_id is None and type_id is None:
        if request.user.is_authenticated:
            user_info = request.user.userinfo
            if user_info.program is not None:
                posts = posts.filter(subject__programs__exact=user_info.program.pk)
                # TODO: Фильтровать по семестру?

    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)

    posts = posts.order_by('created_date').reverse()

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
        'html': render_to_string('cloud/bare_post_list.html', {'posts': posts_page}),
    })
