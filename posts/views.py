from django.http import JsonResponse

from posts.models import Post


def search_posts(request):
    is_approved = request.GET.get('is_approved') in ['True', None]

    posts = Post.objects.all()

    if is_approved or (not is_approved and request.user.is_superuser):
        posts = posts.filter(is_approved=is_approved)

    return JsonResponse([
        post.as_dict() for post in posts
    ], safe=False)


def new_post(request):
    pass
