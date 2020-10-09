from django.contrib import auth
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, redirect

from decorators import auth_required
from website.models import UserInfo, UserStatus


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        user_info = UserInfo(user=instance)
        user_info.status = UserStatus.objects.get(title="Рядовой студент")
        user_info.save()


@receiver(user_logged_in)
def user_info_to_session(sender, user, request, **kwargs):
    request.session['user_avatar_url'] = UserInfo.objects.get(user=user).avatar.url


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


@auth_required
def me(request):
    user_info = UserInfo.objects.get(user=request.user)
    return JsonResponse(user_info.as_dict())
