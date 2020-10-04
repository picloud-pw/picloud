from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404

from cloud.models import Post, Comment
from decorators import auth_required
from website.views.auth import sign_in


@auth_required
def add(request, post_id):
    post_id = request.POST.get("post_id")
    text = request.POST.get("text")

    if text is None or post_id is None:
        return HttpResponse(status=500)

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
def get(request, post_id):
    post_id = request.GET.get('post_id')
    return JsonResponse([
        comment.as_dict() for comment in
        Comment.objects.filter(post_id=post_id).order_by("created_date")
    ], safe=False)


@auth_required
def delete(request, post_id, comment_id):
    if not request.user.is_authenticated:
        return sign_in(request)

    comment = get_object_or_404(Comment, pk=comment_id)
    post_pk = comment.post.pk
    if request.user.is_staff or request.user == comment.author or request.user.is_superuser:
        comment.delete()

    return redirect('post_detail', pk=post_pk)
