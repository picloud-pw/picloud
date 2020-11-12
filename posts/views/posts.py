from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse

from decorators import auth_required
from posts.models import Post
from students.models import StudentInfo

POSTS_PER_PAGE = 12


def can_user_publish_instantly(user):
    if not user.is_authenticated:
        return False
    user_status = user.userinfo.status
    if user_status.can_publish_without_moderation or user.is_superuser or user.is_staff:
        return True
    else:
        return False


def search(request):
    q = request.GET.get('q')
    pk = request.GET.get('id')
    author_id = request.GET.get('author_id')
    subject_id = request.GET.get('subject_id')
    page = request.GET.get('page', 1)
    is_approved = request.GET.get('is_approved') in ['True', None]

    posts = Post.objects.all()

    if is_approved or (not is_approved and request.user.is_superuser):
        posts = posts.filter(is_approved=is_approved)

    if author_id is not None:
        student_info = StudentInfo.objects.get(id=author_id)
        posts = posts.filter(author_id=student_info.user.pk)

    if subject_id is not None:
        posts = posts.filter(subject_id=subject_id)

    if pk is not None:
        posts = posts.filter(id=pk)

    if q is not None:
        posts = posts.filter(title__icontains=q)

    posts = posts.order_by('-created_date')

    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return JsonResponse({'posts': [
        post.as_dict() for post in posts_page
    ]})


@auth_required
def new(request, post_id):
    form = PostForm(request.POST, request.FILES)
    user_can_publish = can_user_publish_instantly(request.user)
    parent_post_id = request.GET.get("parent_post_id")
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
            update_carma(request.user)
            return redirect('post_detail', pk=post.pk)
        else:
            msg = "Спасибо за ваш вклад! Мы уже уведомлены о вашем посте, он будет проверен в ближайшее время."
            return post_detail(request, pk=post.pk, msg=msg)
    return HttpResponse(status=201)


def get(request, post_id):
    pass


@auth_required
def edit(request, post_id):
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
                    update_carma(request.user)
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
        return redirect("cloud")


@auth_required
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if (request.user.is_authenticated and request.user.is_staff) or request.user.pk == post.author.pk:
        update_carma(post.author)
        post.delete()
    return redirect("cloud")


@auth_required
def approve(request, post_id):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Post.objects.filter(pk=pk).update(is_approved=True)
        update_carma(post.author)
        return redirect("moderation")
    else:
        return redirect("cloud")
