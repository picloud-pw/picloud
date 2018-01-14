from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone
from .forms import PostForm
from .forms import UserInfoForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import feedparser
from dateutil import parser


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
            request.session['user_ava_url'] = UserInfo.objects.get(pk=request.user.pk).avatar.url
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
            error = "Не коректно задан логин"
        if len(password) > 20 or len(password) < 5:
            error = "Не коректно задан пароль"
        if email is None or email == "" or len(email) > 20:
            error = "Не корректно задана почта"
        if password != second_password:
            error = "Пароли не совпадают"
        if error == "":
            try:
                User.objects.get(username=username)
                User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username, email, password)
                if first_name is not None:
                    user.first_name = first_name
                if last_name is not None:
                    user.second_name = last_name
                user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                if user_info_form.is_valid():
                    user_info = user_info_form.save(commit=False)
                    user_info.user = request.user
                    user_info.status = UserStatus.objects.get(title="Рядовой студент")
                    user_info.save()
                    request.session['user_ava_url'] = UserInfo.objects.get(pk=request.user.pk).avatar.url
                return redirect('post_list')
            else:
                error = "Такой пользователь уже существует!"
                return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})
        else:
            return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})
    else:
        error = ""
        return render(request, 'auth/sign_up.html', {'error': error, 'user_info_form': user_info_form})


def search(request):
    return render(request, 'search.html', {})


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


def settings(request):
    change_password_form = PasswordChangeForm(request.user)
    user = User.objects.get(pk=request.user.pk)
    user_info = UserInfo.objects.get(user=user)
    return render(request, 'settings.html', {'user': user,
                                             'user_info': user_info,
                                             'change_password_form': change_password_form,
                                             }
                  )


def universities(request):
    univer_list = University.objects.all()
    return render(request, 'universities.html', {"univer_list": univer_list})


def change_password(request):
    return redirect('post_list')
'''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
'''


