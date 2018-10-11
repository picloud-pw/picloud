from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render

from cloud.models import *
from .posts import POSTS_PER_PAGE


def moderation(request):
    if request.user.is_authenticated and (
            request.user.userinfo.status.can_moderate or
            request.user.is_staff or
            request.user.is_superuser):

        posts = Post.objects \
            .filter(is_approved=False) \
            .order_by('created_date')

        page = request.GET.get('page', 1)
        paginator = Paginator(posts, POSTS_PER_PAGE)
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)

        universities = University.objects.filter(is_approved=False)
        departments = Department.objects.filter(is_approved=False)
        chairs = Chair.objects.filter(is_approved=False)
        programs = Program.objects.filter(is_approved=False)
        subjects = Subject.objects.filter(is_approved=False)

        return render(request, 'moderation/moderation.html', {
            'posts': posts_page,
            'universities': universities,
            'departments': departments,
            'chairs': chairs,
            'programs': programs,
            'subjects': subjects,
        })

    else:
        return redirect("cloud")
