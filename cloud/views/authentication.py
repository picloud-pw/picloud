from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from cloud.models import UserInfo
import requests

from cloud.models import UserInfo

VK_ID = '6477166'
VK_API_VERSION = '5.74'
VK_SECRET = 'loqcCdT0JDj5fTrQd0ku'


def user_info_to_session(request, user):
    request.session['user_avatar_url'] = UserInfo.objects.get(user=user).avatar.url
    program = UserInfo.objects.get(user=user).program
    if program is not None:
        request.session['program_id'] = program.pk
    else:
        request.session['program_id'] = ""


def sign_out(request):
    auth.logout(request)
    return redirect("index")


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)

            user_info_to_session(request, user)

            return redirect('cloud')
        else:
            error = "Неверно введены логин или пароль!"
            return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(),})
    else:
        error = ""
        return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(),})


def vk_auth(request):
    code = request.GET["code"]
    URL = 'https://oauth.vk.com/access_token?' \
          'client_id=' + VK_ID + \
          '&client_secret=' + VK_SECRET + \
          '&code=' + code + \
          '&redirect_uri=' + request.get_host() + '/vk_auth/'
    if request.user.is_authenticated:
        if code is not None:
            data = requests.get(URL).json()
            vk_id = data['user_id']
            user_info = UserInfo.objects.get(user=request.user)
            user_info.vk_id = vk_id
            user_info.save()
            return redirect("settings")
        else:
            error = request.GET('error_description')
            return render(request, 'settings.html', {'error': error, 'host': request.get_host() })
    else:
        if code is not None:
            data = requests.get(URL).json()
            vk_id = data['user_id']
            user_info = UserInfo.objects.filter(vk_id=vk_id)
            if user_info.count():
                user = user_info.first().user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                user_info_to_session(request, user)
                return redirect("cloud")
            else:
                error = "Ваша ВК старница не привязана ни к одному пользователю PiCloud! Для начала авторизуйтесь."
                return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(), })
        else:
            error = request.GET('error_description')
            return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(), })


def del_vk_id(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=request.user)
        user_info.vk_id = None
        user_info.save()
        return redirect("settings")
    else:
        return redirect("signin")
