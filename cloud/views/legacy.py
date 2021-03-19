from django.shortcuts import redirect

from cloud.models import Post as OldPost
from posts.models import Post as NewPost


def post_page_redirect(request, post_id):
    old_post = OldPost.objects.get(id=post_id)
    new_post = NewPost.objects.filter(
        title=old_post.title,
        text=old_post.text,
        created_date=old_post.created_date,
    )
    return redirect(f'/posts?id={new_post.first().id}')
