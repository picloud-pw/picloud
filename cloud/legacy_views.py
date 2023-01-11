from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

from cloud.models import Post as OldPost
from cloud.models import University, Program, Subject as OldSubject
from posts.models import Post as NewPost

from students.models import StudentInfo
from hierarchy.models import Department, Subject as NewSubject


def post_page_redirect(request, post_id):
    old_post = OldPost.objects.get(id=post_id)
    new_post = NewPost.objects.filter(
        title=old_post.title,
        text=old_post.text,
        created_date=old_post.created_date,
    )
    return redirect(f'/posts/{new_post.first().id}/', permanent=True)


def program_page(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    new_program = Department.objects.filter(
        department_type__name='Program',
        name=program.title,
    )
    if len(new_program):
        return redirect(f'/deps/{new_program.first().id}/', permanent=True)
    else:
        return redirect('/deps/', permanent=True)


def subject_page(request, subject_id):
    subject = get_object_or_404(OldSubject, pk=subject_id)
    new_subject = NewSubject.objects.filter(
        name=subject.title,
        semester=subject.semester,
    )
    if len(new_subject):
        return redirect(f'/subs/{new_subject.first().id}/')
    else:
        return redirect('cloud')


def universities_list(request):
    return redirect('/deps/', permanent=True)


def university_page(request, university_id):
    university = get_object_or_404(University, pk=university_id)
    new_university = Department.objects.filter(
        department_type__name='University',
        name=university.short_title,
    )
    if len(new_university):
        return redirect(f'/deps/{new_university.first().id}/')
    else:
        return redirect('/deps/', permanent=True)


def students_from_university(request, university_id):
    return redirect('students')


def user_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_info = StudentInfo.objects.get(user=user)
    return redirect(f'/studs/{user_info.id}/')


def user_posts(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_info = StudentInfo.objects.get(user=user)
    return redirect(f'/studs/{user_info.id}/')


def user_not_checked_posts(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_info = StudentInfo.objects.get(user=user)
    return redirect(f'/studs/{user_info.id}/')


def settings_page(request):
    return redirect('profile')


def feed_page(request):
    return redirect('cloud')


def auth_signin(request):
    return redirect('signin')
