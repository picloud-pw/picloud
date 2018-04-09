from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from cloud.models import UserInfo


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

            request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
            program = UserInfo.objects.get(user=user).program
            if program is not None:
                request.session['program_id'] = program.pk
            else:
                request.session['program_id'] = ""

            return redirect('post_list')
        else:
            error = "Неверно введены логин или пароль!"
            return render(request, 'auth/signin.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/signin.html', {'error': error})


