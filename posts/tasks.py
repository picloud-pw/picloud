from posts.models import Post, Attachment


def migrate_attachments():
    for post in Post.objects.all():
        if post.link is not None:
            Attachment.objects.create(
                post=post,
                link=post.link,
            )
        if post.image:
            Attachment.objects.create(
                post=post,
                image=post.image,
            )
        if post.file:
            Attachment.objects.create(
                post=post,
                file=post.file,
            )
