import os

import bleach
import markdown
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone

from hierarchy.models import Subject
from students.models import StudentInfo


class PostType(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=256, null=False, unique=True)
    plural = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'plural': self.plural,
        }


class Post(models.Model):
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(PostType, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    parent_post = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    last_editor = models.ForeignKey(User, related_name='last_editor', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    ALLOWED_HTML_TAGS = allowed_html_tags = bleach.ALLOWED_TAGS + [
        u'h1', u'h2', u'h3', u'h4', u'p', u'a', u'li', u'ul', u'ol', u'pre', u'code', u'hr', u'br', u'strong',
    ]

    def __str__(self):
        return f"{'[DRAFT]' if self.is_draft else ''} " \
               f"{'[MODER]' if not self.is_approved and not self.is_draft else ''} " \
               f"{self.author.username} - {self.title}"

    def html(self):
        if self.text is None:
            return ""
        dangerous_html = markdown.markdown(self.text, extensions=['markdown.extensions.fenced_code'])
        safe_html = bleach.clean(dangerous_html, tags=self.ALLOWED_HTML_TAGS)
        html_with_hyperlinks = bleach.linkify(safe_html)
        return html_with_hyperlinks

    def is_valid(self):
        if self.title is None or len(self.title) < 5:
            raise ValueError("Title length shorten than 5 symbols.")
        if self.subject is None:
            raise ValueError("Subject is not set.")
        if self.type is None:
            raise ValueError("Post Type is not set.")
        return True

    def can_be_edited_by(self, user):
        return self.author == user or \
               user.userinfo.status.can_moderate or \
               user.is_staff() or \
               user.is_superuser()

    def is_parent(self):
        return self.post_set.count() > 0

    def get_childs(self):
        return self.post_set

    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    def created_date_human(self):
        import datetime
        import pytz
        timezone = pytz.timezone('Europe/Moscow')
        date = self.created_date.astimezone(timezone)
        today = datetime.date.today()
        if datetime.datetime.now(tz=timezone) - date < datetime.timedelta(minutes=1):
            return "Только что"
        if date.date() == today:
            return date.strftime("сегодня %H:%M")
        if date.date() == today - datetime.timedelta(days=1):
            return date.strftime("вчера %H:%M")
        if today - date.date() < datetime.timedelta(days=5):
            return date.strftime("%A ").lower() + date.strftime("%H:%M")
        if date.year == today.year:
            return date.strftime("%d %b %H:%M")
        return date.strftime("%d %b %Y %H:%M")

    def get_attachments(self):
        return {
            'images': [i.as_dict()['image'] for i in Attachment.objects.filter(post=self).filter(~Q(image=''))],
            'files': [i.as_dict()['file'] for i in Attachment.objects.filter(post=self).filter(~Q(file=''))],
            'links': [i.as_dict()['link'] for i in Attachment.objects.filter(post=self, link__isnull=False)],
        }

    def as_dict(self):
        student_info = StudentInfo.objects.get(user=self.author)
        return {
            "id": self.pk,
            "parent_post": self.parent_post.id if self.parent_post is not None else None,
            "is_parent": self.is_parent(),
            "author": student_info.as_dict(),
            "author_id": self.author.pk,
            "title": self.title,
            "text": self.text,
            "html": self.html(),
            "created_date": self.created_date,
            "created_date_human": self.created_date_human(),
            "subject": self.subject.as_dict() if self.subject is not None else None,
            "type": self.type.as_dict() if self.type is not None else None,
            "views": self.views,
            "comments": self.get_comment_count(),
            "attachments": self.get_attachments(),
        }


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True, default=None)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True, default=None)
    link = models.URLField(max_length=512, null=True, blank=True, default=None)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ""

    def get_image_width(self):
        if not self.image:
            return None
        try:
            return self.image.width
        except IOError or FileNotFoundError:
            return None

    def get_image_height(self):
        if not self.image:
            return None
        try:
            return self.image.height
        except IOError or FileNotFoundError:
            return None

    def get_file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
        else:
            return ""

    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].upper()
        else:
            return None

    def __str__(self):
        return f"[{self.post.pk}] " \
               f"{'image - ' + self.image.name if self.image else ''}" \
               f"{'file - ' + self.file.name if self.file else ''}" \
               f"{'link - ' + self.link if self.link else ''}"

    def as_dict(self):
        dictionary = dict()
        if self.file is not None:
            dictionary['file'] = {
                "url": self.get_file_url(),
                "extension": self.file_extension(),
            }
        if self.image is not None:
            dictionary['image'] = {
                "url": self.get_image_url(),
                "width": self.get_image_width(),
                "height": self.get_image_height(),
            }
        if self.link is not None:
            dictionary['link'] = self.link
        return dictionary


class Comment(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author.username} - {self.text}"

    def get_author_avatar_url(self):
        user_info = StudentInfo.objects.get(user=self.author)
        return user_info.avatar.url

    def as_dict(self):
        return {
            "id": self.pk,
            "post_id": self.post.pk,
            "author": {
                "id": StudentInfo.objects.get(user=self.author).pk,
                "username": self.author.username,
                "avatar": self.get_author_avatar_url(),
            },
            "text": self.text,
            "created_date": self.created_date,
        }
