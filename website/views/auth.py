from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect

from students.models import StudentInfo, StudentStatus


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    default_student_status = StudentStatus.objects.get(title="Рядовой студент")
    StudentInfo.objects.get_or_create(
        user=instance,
        defaults={
            'status': default_student_status,
        }
    )


def update_avatar(backend, strategy, details, response, user=None, * args, ** kwargs):
    try:
        if user is None:
            raise ValueError
        user_info = StudentInfo.objects.get(user=user)
    except (ObjectDoesNotExist, ValueError):
        return

    url = None
    if backend.name == 'facebook':
        url = f"https://graph.facebook.com/{response['id']}/picture?width=150&height=150"
    # if backend.name == 'twitter':
    #     url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['picture']
    # if backend.name == 'instagram':
    #     url = response['profile_pic_url']
    if backend.name == 'vk-oauth2':
        url = response['photo']
    if backend.name == 'github':
        url = response['avatar_url']
    if url and user_info.avatar_url is None:
        user_info.avatar_url = url
        user_info.save()



def sign_in(request):
    return render(request, 'sign_in.html')


def sign_out(request):
    auth.logout(request)
    return redirect("index")


def after_login(request):
    next_page = request.GET.get("next")
    if next_page is not None:
        return redirect(next_page)
    else:
        return redirect('index')
