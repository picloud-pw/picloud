from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect, render

from cloud.models import UserInfo


@receiver(user_logged_in)
def user_info_to_session(sender, user, request, **kwargs):
    request.session['user_avatar_url'] = UserInfo.objects.get(user=user).avatar.url
    program = UserInfo.objects.get(user=user).program
    request.session['program_id'] = program.pk if program is not None else ""


def sign_out(request):
    auth.logout(request)
    return redirect("index")


def sign_in(request, msg=None, error=None):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )

        if user is not None and user.is_active:
            login(request, user)
            return redirect('cloud')
        else:
            error = "Неверно введены логин или пароль!"
            return render(request, 'auth/signin.html', locals())
    else:
        return render(request, 'auth/signin.html', locals())


def after_login(request):
    next_page = request.GET.get("next")
    if next_page is not None:
        return redirect(next_page)
    else:
        return redirect('index')
