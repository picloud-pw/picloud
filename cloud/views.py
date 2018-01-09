from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
        form = PostForm(request.POST)
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
        form = PostForm(request.POST, instance=post)
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
            return redirect('post_list')
        else:
            error = "Не верно введены логин или пароль!"
            return render(request, 'auth/sign_in.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/sign_in.html', {'error': error})


def sign_up(request):
    if request.method == "POST":
        error = ""
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        second_password = request.POST['second_password']
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
                return redirect('post_list')
            else:
                error = "Такой пользователь уже существует!"
                return render(request, 'auth/sign_up.html', {'error': error})
        else:
            return render(request, 'auth/sign_up.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/sign_up.html', {'error': error})


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
    return render(request, 'settings.html', {})