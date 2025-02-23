import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse

from decorators import auth_required
from hierarchy.models import Subject
from posts.models import Post, PostType
from students.models import StudentInfo


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
    page_size = request.GET.get('page_size', 12)
    is_draft = request.GET.get('is_draft') not in ['False', None]
    is_approved = request.GET.get('is_approved') in ['True', None]

    posts = Post.objects.all()

    if is_draft:
        posts = posts.filter(is_draft=True, author_id=request.user.id)
    else:
        posts = posts.filter(is_draft=False)
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

    paginator = Paginator(posts, page_size)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts_page = paginator.page(page)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return JsonResponse({
        'posts': [
            post.as_dict() for post in posts_page
        ],
        'total_posts': paginator.count,
        'page': int(page),
        'page_size': page_size,
        'total_pages': paginator.num_pages,
    })


@auth_required
def new(request):
    post_draft = Post.objects.create(
        author=request.user,
        is_draft=True,
    )
    return JsonResponse(post_draft.as_dict())


@auth_required
def update(request):
    post_id = request.POST.get('id')
    if post_id is None:
        return HttpResponse(status=404)
    post = Post.objects.get(id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponse(status=403)

    subject_id = request.POST.get('subject_id')
    if subject_id is not None:
        post.subject = Subject.objects.get(id=subject_id)
    post_type_id = request.POST.get('post_type_id')
    if post_type_id is not None:
        post.type = PostType.objects.get(id=post_type_id)
    title = request.POST.get('title')
    if title is not None:
        post.title = title
    text = request.POST.get('text')
    if text is not None:
        post.text = text
    body = request.POST.get('body')
    if body is not None:
        parsed_body = json.loads(body)
        post.ejs_body = parsed_body
    post.last_editor = request.user
    post.save()
    return HttpResponse(status=200)


def get(request):
    post_id = request.GET.get('id')
    if post_id is None:
        return HttpResponse(status=404)
    post = Post.objects.get(id=post_id)
    if post.author == request.user or \
            request.user.is_superuser or request.user.is_staff or \
            (not post.is_draft and post.is_approved):
        post.views += 1
        post.save()
        return JsonResponse(post.as_dict())
    else:
        return HttpResponse(status=403)


@auth_required
def submit(request):
    post_id = request.POST.get('id')
    if post_id is None:
        return HttpResponse(status=404)
    post = Post.objects.get(id=post_id)

    is_draft = request.POST.get('is_draft')
    if is_draft is None:
        return HttpResponse(status=400)

    if not ((request.user.is_authenticated and request.user.is_staff)
            or request.user.pk == post.author.pk):
        return HttpResponse(status=403)

    if is_draft == 'False':
        try:
            post.is_draft = False if post.is_valid() else True
        except ValueError as e:
            return JsonResponse({'error': str(e)})
    else:
        post.is_draft = True

    post.save()
    return HttpResponse(status=200)


@auth_required
def delete(request):
    post_id = request.POST.get('id')
    if post_id is None:
        return HttpResponse(status=404)
    post = Post.objects.get(id=post_id)
    if (request.user.is_authenticated and request.user.is_staff) \
            or request.user.pk == post.author.pk:
        post.delete()
    return HttpResponse(status=200)


@auth_required
def approve(request):
    post_id = request.POST.get('id')
    if post_id is None:
        return HttpResponse(status=404)
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated and \
            (request.user.is_staff or request.user.is_superuser):
        post.is_approved = True
        post.save()
    return HttpResponse(status=200)
