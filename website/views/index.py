from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from students.models import StudentInfo


def index(request):
    if request.user.is_authenticated:
        return redirect('cloud')
    else:
        return redirect('about')


def robots(request):
    return render(request, 'robots.txt', content_type="text/plain")


def about(request):
    return render(request, 'index.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def cloud_page(request):
    return render(request, 'cloud.html')


def post_page_redirect(request):
    post_id = request.GET.get('id')
    return redirect("post_page", post_id=post_id, permanent=True)


def post_page(request, post_id):
    return render(request, 'posts.html')


def post_edit_page(request, post_id):
    return render(request, 'edit_post_page.html')


def redirect_subject_page(request):
    sub_id = request.GET.get('id')
    return redirect("subjects_page", sub_id=sub_id, permanent=True)


def subject_page(request, sub_id):
    return render(request, 'subjects.html')


def departments_page_redirect(request):
    dep_id = request.GET.get('id')
    if dep_id is not None:
        return redirect("departments_page", dep_id=dep_id, permanent=True)
    else:
        return redirect("root_departments_page", permanent=True)


def root_departments_page(request):
    return render(request, 'departments.html')


def departments_page(request, dep_id):
    return render(request, 'departments.html')


@login_required(login_url='/signin/')
def moderation_page(request):
    return render(request, 'moderation.html')


@login_required(login_url='/signin/')
def chats_page(request):
    return render(request, 'chats.html')


@login_required(login_url='/signin/')
def new_post_page(request):
    return render(request, 'new_post_page.html')


@login_required(login_url='/signin/')
def profile_page(request, username):
    return render(request, 'profile.html')


@login_required(login_url='/signin/')
def settings_page(request):
    return render(request, 'settings.html')


@login_required(login_url='/signin/')
def redirect_students_page(request):
    stud_id = request.GET.get('id')
    if stud_id is not None:
        return redirect("students_page", stud_id=stud_id, permanent=True)
    else:
        return redirect("root_students_page", permanent=True)


@login_required(login_url='/signin/')
def root_students_page(request):
    return render(request, 'students.html')


@login_required(login_url='/signin/')
def students_page(request, stud_id):
    userinfo = StudentInfo.objects.filter(id=stud_id).first()
    return redirect("profile", username=userinfo.user.username, permanent=True)


@login_required(login_url='/signin/')
def memes_page(request):
    return render(request, 'memes.html')
