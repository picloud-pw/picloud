from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse

from cloud.models import Post, Comment
from decorators import auth_required


@auth_required
def add(request):
    post_id = request.POST.get("post_id")
    text = request.POST.get("text")

    if text is None or post_id is None:
        return HttpResponse(status=400)
    try:
        post = Post.objects.get(pk=post_id)
        new_comment = Comment(
                author=request.user,
                post=post,
                text=text,
            )
        new_comment.save()
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': e})
    return HttpResponse(status=200)


@auth_required
def get(request):
    post_id = request.GET.get('post_id')
    return JsonResponse({
        "comments": [
            comment.as_dict() for comment in
            Comment.objects.filter(post_id=post_id).order_by("created_date")
        ]
    })


@auth_required
def delete(request):
    comment_id = request.POST.get('id')
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.author or \
            request.user.is_staff or request.user.is_superuser:
        comment.delete()
    return HttpResponse(status=200)
