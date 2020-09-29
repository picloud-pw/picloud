from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from cloud.forms import *
from cloud.models import Post
from posts.views.posts import POSTS_PER_PAGE


def post_list(request, displayed_posts=None):
    empty_message = ""
    posts = Post.objects \
        .filter(is_approved=True) \
        .filter(parent_post=None) \
        .filter(created_date__lte=timezone.now())

    if request.user.is_authenticated:
        user_info = request.user.userinfo
        if user_info.program is not None:
            posts = posts.filter(subject__programs__exact=user_info.program.pk)
        if displayed_posts is not None:
            # TODO: Возможно, небезопасное использование параметра запроса
            # Может ли пользователь таким образом запросить запрещённый пост?
            # Возможно, следует использовать пересечение (QuerySet.intersection).
            posts = displayed_posts
            empty_message = "Данный пользователь пока не поделился своими материалами."

    posts = posts \
        .order_by('created_date') \
        .reverse()

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'cloud/post_list.html', {
        'posts': posts_page,
        'empty_message': empty_message
    })
