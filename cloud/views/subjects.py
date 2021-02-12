from django.shortcuts import get_object_or_404, render, redirect

from cloud.forms import NewSubjectForm
from cloud.models import Subject, Post
from cloud.views.message import message
from posts.views.posts import can_user_publish_instantly


def subject_page(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    posts = Post.objects.filter(subject=subject).filter(is_approved=True).filter(parent_post=None)
    post_types = set()
    for post in posts:
        post_types.add(post.type)
    return render(request, "structure/subject_page.html", {
        "subject": subject,
        "posts": posts,
        "post_types": post_types,
    })


def new_subject(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

            new_subject = NewSubjectForm(request.POST)
            if new_subject.is_valid():
                subject = new_subject.save(commit=False)
                subject.is_approved = can_user_publish_instantly(request.user)
                subject.save()
                return message(request, success_msg)
            else:
                return message(request, 'Одно из полей формы "Предмет" заполнено некорректно')
        else:
            new_subject = NewSubjectForm()
            return render(request, 'structure/new/subject.html', {'new_subject': new_subject})
    else:
        return redirect("signin")


def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        subject.delete()
    return redirect("moderation")


def subject_approve(request, subject_id):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Subject.objects.filter(pk=subject_id).update(is_approved=True)
        return redirect("moderation")
    else:
        return redirect("cloud")
