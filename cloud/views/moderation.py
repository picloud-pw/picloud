from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render

from cloud.models import *
from .posts import POSTS_PER_PAGE
from . import NOT_VALID


def moderation(request):
    if request.user.is_authenticated and (
            request.user.userinfo.status.can_moderate or
            request.user.is_staff or
            request.user.is_superuser):

        posts = Post.objects \
            .filter(approved=False) \
            .order_by('created_date')

        page = request.GET.get('page', 1)
        paginator = Paginator(posts, POSTS_PER_PAGE)
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)

        universities = University.objects.filter(validate_status=NOT_VALID)
        departments = Department.objects.filter(validate_status=NOT_VALID)
        chairs = Chair.objects.filter(validate_status=NOT_VALID)
        programs = Program.objects.filter(validate_status=NOT_VALID)
        subjects = Subject.objects.filter(validate_status=NOT_VALID)

        return render(request, 'moderation.html', {
            'posts': posts_page,
            'universities': universities,
            'departments': departments,
            'chair': chairs,
            'programs': programs,
            'subjects': subjects,
        })

    else:
        return redirect("post_list")
