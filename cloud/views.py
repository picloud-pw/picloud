from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import feedparser
from dateutil import parser
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
from django.core.mail import EmailMessage
import json


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'cloud/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'cloud/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'cloud/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'cloud/post_edit.html', {'form': form})


def message(request, msg):
    return render(request, 'message.html', {message: msg})


def sign_out(request):
    auth.logout(request)
    return redirect("post_list")


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
            return redirect('post_list')
        else:
            error = "Не верно введены логин или пароль!"
            return render(request, 'auth/sign_in.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/sign_in.html', {'error': error})


def sign_up(request):
    user_info_form = UserInfoForm()
    if request.method == "POST":
        error = ""
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        second_password = request.POST['second_password']
        user_info_form = UserInfoForm(request.POST, request.FILES)

        if len(username) > 10 or len(username) < 5:
            error = "Некорректно задан логин"
        if len(password) < 5:
            error = "Некорректно задан пароль"
        if email is None or email == "" or len(email) > 128:
            error = "Некорректно задана почта"
        if password != second_password:
            error = "Пароли не совпадают"
        if error == "":
            if not (User.objects.filter(username__iexact=username).exists() or
                    User.objects.filter(email__iexact=email).exists()):
                if user_info_form.is_valid():

                    # заполнение основной информации
                    user = User.objects.create_user(username, email, password)
                    if first_name is not None:
                        user.first_name = first_name
                    if last_name is not None:
                        user.second_name = last_name
                    user.is_active = False
                    user.save()
                    # дополнительная информация
                    user_info = user_info_form.save(commit=False)
                    user_info.user = user
                    user_info.status = UserStatus.objects.get(title="Рядовой студент")
                    user_info.save()

                    # подтверждение почты
                    current_site = get_current_site(request)
                    mail_subject = 'Активация PiCloud аккаунта'
                    msg = render_to_string('auth/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': user.pk,
                        'token': account_activation_token.make_token(user),
                    })
                    email = EmailMessage(mail_subject, msg, to=[email])
                    email.send()
                    msg = 'Пожалуйста подтвердите адрес элетронной почты для завершения регистрации'
                    return render(request, 'message.html', {'message': msg})
                else:
                    error = "Не все поля формы прошли валидацию!"
                    return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})
            else:
                error = "Такой пользователь уже существует!"
                return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})
        else:
            return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})
    else:
        error = ""
        return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
        msg = 'Почта подтверждена! Теперь вы можете заходить в свой личный кабинет!'
        return render(request, 'message.html', {'message': msg})
    else:
        msg = 'Ссылка не корректна! Обратитесь в службу обратной связи с этой проблемой!'
        return render(request, 'message.html', {'message': msg})


def search(request):
    university = ChooseUniversityForm()
    department = ChooseDepartmentForm()
    chair = ChooseChairForm()
    program = ChooseProgramForm()
    subject = ChooseSubjectForm()
    return render(request, 'search.html', {'university': university,
                                           'department': department,
                                           'chair': chair,
                                           'program': program,
                                           'subject': subject,
                                           })


vk_urls_rss = [
    "http://feed.exileed.com/vk/feed/pashasmeme/?owner=1&only_admin=1",
    "http://feed.exileed.com/vk/feed/dnische1/?owner=1&only_admin=1",
    "http://feed.exileed.com/vk/feed/itmoquotepad/?owner=1&only_admin=1",
    "http://feed.exileed.com/vk/feed/wisemrduck/?owner=1&only_admin=1",
    "http://feed.exileed.com/vk/feed/klimenkovdefacto/?owner=1&only_admin=1",
]
feeds_rss = []
for url in vk_urls_rss:
    feeds_rss.extend(feedparser.parse(url)["entries"])


def memes(request):
    feed_col_1 = []
    feed_col_2 = []
    counter = 0
    for feed in feeds_rss:
        feed["published"] = parser.parse(feed.published).strftime("%d.%m.%y %H:%M")
        if counter % 2 == 0:
            feed_col_1.append(feed)
        else:
            feed_col_2.append(feed)
        counter += 1
    feeds = [feed_col_1, feed_col_2]
    return render(request, 'memes.html', {'colomns_feed': feeds})


def settings(request, message=""):
    change_avatar_form = AvatarChangeForm()
    change_password_form = PasswordChangeForm(request.user)
    user = User.objects.get(pk=request.user.pk)
    user_info = UserInfo.objects.get(user=user)
    return render(request, 'settings.html', {'user': user,
                                             'user_info': user_info,
                                             'change_password_form': change_password_form,
                                             'change_avatar_form': change_avatar_form,
                                             'message': message,
                                             }
                  )


def universities(request):
    univer_list = University.objects.all()
    return render(request, 'universities.html', {"univer_list": univer_list})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return settings(request, message='Пароль успешно изменен!')
        else:
            return settings(request, message='Пароли введены с ошибкой!')
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings(request, message='Пароль должен быть длиннее 8 символов!')


def change_avatar(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST,
                                request.FILES,
                                instance=UserInfo.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            request.session['user_ava_url'] = UserInfo.objects.get(user=request.user).avatar.url
            return settings(request)
        else:
            return settings(request)
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings(request)


def get_departments(request):
    university_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Department.objects.filter(university=university_id)]
    return JsonResponse(dictionaries, safe=False)


def get_chairs(request):
    department_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Chair.objects.filter(department=department_id)]
    return JsonResponse(dictionaries, safe=False)


def get_programs(request):
    chair_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Program.objects.filter(chair=chair_id)]
    return JsonResponse(dictionaries, safe=False)


def get_subjects(request):
    program_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Subject.objects.filter(programs=program_id)]
    return JsonResponse(dictionaries, safe=False)
