from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib import auth


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


def signin(request):
    return render(request, 'auth/signin.html', {})


def signout(request):
    return render(request, 'auth/signout.html', {})


def signup(request):
    return render(request, 'auth/signup.html', {})


def search(request):
    return render(request, 'search.html', {})


def memes(request):
    return render(request, 'memes.html', {})
