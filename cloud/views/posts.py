from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from cloud.forms import *
from cloud.models import UserInfo, Post

POSTS_PER_PAGE = 12


def can_user_publish_instantly(user):
    if not user.is_authenticated:
        return False
    user_status = user.userinfo.status
    if user_status.can_publish_without_moderation or user.is_superuser or user.is_staff:
        return True
    else:
        return False


def post_list(request, displayed_posts=None):
    empty_message = ""
    posts = Post.objects \
        .filter(is_approved=True) \
        .filter(parent_post=None) \
        .filter(created_date__lte=timezone.now())

    if request.user.is_authenticated:
        user_info = request.user.userinfo
        if user_info.program is not None:
            posts = posts.filter(subject__programs__exact=user_info.program.pk)
            # TODO: Фильтровать по семестру?
        if displayed_posts is not None:
            # TODO: Возможно, небезопасное использование параметра запроса
            # Может ли пользователь таким образом запросить запрещённый пост?
            # Возможно, следует использовать пересечение (QuerySet.intersection).
            posts = displayed_posts
            empty_message = "Данный пользователь пока не поделился своими материалами."

    posts = posts \
        .order_by('created_date') \
        .reverse()

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'cloud/post_list.html', {
        'posts': posts_page,
        'empty_message': empty_message
    })


def post_detail(request, pk, msg=""):
    post = get_object_or_404(Post, pk=pk)
    child_posts = Post.objects.filter(parent_post=post)
    if post.views < 99999:
        post.views += 1
        post.save()
    return render(request, 'cloud/post_detail.html', {
        'post': post,
        'child_posts': child_posts,
        'message': msg
    })


def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            user_can_publish = can_user_publish_instantly(request.user)
            parent_post_id = request.GET.get("parent_post_id", None)
            if form.is_valid():
                post = form.save(commit=False)
                post.last_editor = request.user
                post.author = request.user
                post.created_date = timezone.now()
                post.is_approved = user_can_publish
                if parent_post_id is not None:
                    post.parent_post = Post.objects.get(pk=parent_post_id)
                post.save()
                request.session['last_post_subject'] = request.POST["subject"]
                if user_can_publish:
                    return redirect('post_detail', pk=post.pk)
                else:
                    msg = "Спасибо за ваш вклад! Мы уже уведомлены о вашем посте, он будет проверен в ближайшее время."
                    return post_detail(request, pk=post.pk, msg=msg)
            else:
                form = PostForm()
                user_info = get_object_or_404(UserInfo, user=request.user)
                return render(request, 'cloud/post_edit.html', {'form': form, 'user_info': user_info})
        else:
            form = PostForm()
            user_info = get_object_or_404(UserInfo, user=request.user)
            return render(request, 'cloud/post_edit.html', {'form': form, 'user_info': user_info})
    else:
        return redirect("signin")


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (request.user.is_authenticated and request.user.is_staff) or request.user.pk == post.author.pk:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            user_can_publish = can_user_publish_instantly(request.user)
            if form.is_valid():
                post = form.save(commit=False)
                post.last_editor = request.user
                post.published_date = timezone.now()
                post.is_approved = user_can_publish
                post.save()
                if user_can_publish:
                    return redirect('post_detail', pk=post.pk)
                else:
                    msg = "Благодарим за правки! В ближайшее время мы проверим и опубликуем их."
                    return post_detail(request, pk=post.pk, msg=msg)
            else:
                form = PostForm(instance=post)
                user_info = get_object_or_404(UserInfo, user=request.user)
                return render(request, 'cloud/post_edit.html', {
                    'form': form,
                    'post': post
                })
        else:
            form = PostForm(instance=post)
            user_info = get_object_or_404(UserInfo, user=request.user)
            return render(request, 'cloud/post_edit.html', {
                'form': form,
                'post': post,
            })
    else:
        return redirect("post_list")


def post_new_child(request, pk):
    return redirect("/post/new/?parent_post_id=" + str(pk))


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (request.user.is_authenticated and request.user.is_staff) or request.user.pk == post.author.pk:
        post.delete()
    return redirect("post_list")


def post_checked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Post.objects.filter(pk=pk).update(is_approved=True)
        return redirect("moderation")
    else:
        return redirect("post_list")


def search(request):
    university = ChooseUniversityForm()
    department = ChooseDepartmentForm()
    chair = ChooseChairForm()
    program = ChooseProgramForm()
    subject = ChooseSubjectForm()
    user_info = UserInfo.objects.filter(user=request.user.pk).first()
    return render(request, 'search.html', {
        'university': university,
        'department': department,
        'chair': chair,
        'program': program,
        'subject': subject,
        'user_info': user_info,
    })
