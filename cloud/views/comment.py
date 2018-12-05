from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from cloud.models import Post, Comment
from cloud.views.authentication import sign_in


def create_comment(request, post_pk):
    if not request.user.is_authenticated:
        return sign_in(request, msg="Пожалуйста, авторизуйтесь для добавления комментариев.")

    if request.method != "POST":
        return HttpResponse(status=404)

    text = request.POST.get("comment_text", None)

    if text is not None:
        post = Post.objects.get(pk=post_pk)
        new_comment = Comment(author=request.user, post=post, text=text)
        new_comment.save()

    return redirect('post_detail', pk=post_pk)


def delete_comment(request, comment_pk):
    if not request.user.is_authenticated:
        return sign_in(request, msg="Пожалуйста, авторизуйтесь для удаления комментариев.")

    comment = get_object_or_404(Comment, pk=comment_pk)
    post_pk = comment.post.pk
    if request.user.is_staff or request.user == comment.author or request.user.is_superuser:
        comment.delete()

    return redirect('post_detail', pk=post_pk)


def get_comments(request, comment_pk):
    comments = Comment.objects.filter(pk=comment_pk)
    if comments.count() == 1:
        return redirect('post_detail', pk=comments.first.pk)
    else:
        return redirect('feed')
