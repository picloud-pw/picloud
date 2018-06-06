from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
import requests

from cloud.models import UserInfo

VK_ID = '6477166'
VK_API_VERSION = '5.74'
VK_SECRET = 'loqcCdT0JDj5fTrQd0ku'


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

            request.session['user_avatar_url'] = UserInfo.objects.get(user=user).avatar.url
            program = UserInfo.objects.get(user=user).program
            if program is not None:
                request.session['program_id'] = program.pk
            else:
                request.session['program_id'] = ""

            return redirect('cloud')
        else:
            error = "Неверно введены логин или пароль!"
            return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(),})
    else:
        error = ""
        return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(),})


def vk_auth(request):
    code = request.GET["code"]
    if code is not None:
        URL = 'https://oauth.vk.com/access_token?' \
              'client_id=' + VK_ID + \
              '&client_secret=' + VK_SECRET + \
              '&code=' + code + \
              '&redirect_uri=' + request.get_host() + '/vk_auth/'
        data = requests.get(URL).json()
        token = data['access_token']
        user_id = data['user_id']
        return redirect("cloud")
    else:
        error = request.GET('error_description')
        return render(request, 'auth/signin.html', {'error': error, 'host': request.get_host(), })
