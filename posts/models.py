import os

import bleach
import markdown
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from cloud.models import UserInfo
from hierarchy.models import Subject


class PostType(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=256, null=False, unique=True)
    plural = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'title': self.title,
            'plural': self.plural,
        }


class Post(models.Model):
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(PostType, on_delete=models.CASCADE)
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
    is_approved = models.BooleanField(default=False)

    ALLOWED_HTML_TAGS = allowed_html_tags = bleach.ALLOWED_TAGS + [
        u'h1', u'h2', u'h3', u'h4', u'p', u'a', u'li', u'ul', u'ol', u'pre', u'code', u'hr', u'br', u'strong',
    ]

    def __str__(self):
        return self.title

    def html(self):
        dangerous_html = markdown.markdown(self.text, extensions=['markdown.extensions.fenced_code'])
        safe_html = bleach.clean(dangerous_html, tags=self.ALLOWED_HTML_TAGS)
        html_with_hyperlinks = bleach.linkify(safe_html)
        return html_with_hyperlinks

    def publish(self):
        self.created_date = timezone.now()
        self.save()

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

    def can_be_edited_by(self, user):
        return self.author == user or \
               user.userinfo.status.can_moderate or \
               user.is_staff() or \
               user.is_superuser()

    def is_parent(self):
        return self.post_set.count() > 0

    def get_childs(self):
        return self.post_set

    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].upper()
        else:
            return None

    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    def created_date_human(self):
        import datetime
        import pytz
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
        except Exception as e:
            # for mac os
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
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

    def as_dict(self):
        return {
            "id": self.pk,
            "parent_post": self.parent_post.id if self.parent_post is not None else None,
            "is_parent": self.is_parent(),
            "author": {
                "id": self.author.id,
                "username": self.author.username,
            },
            "author_id": self.author.pk,
            "title": self.title,
            "text": self.text,
            "html": self.html(),
            "created_date": self.created_date,
            "created_date_human": self.created_date_human(),
            "subject": self.subject.as_dict() if self.subject is not None else None,
            "type": self.type.as_dict(),
            "link": self.link,
            "image": {
                "url": self.get_image_url(),
                "width": self.get_image_width(),
                "height": self.get_image_height(),
            },
            "file": {
                "url": self.get_file_url(),
                "extension": self.file_extension(),
            },
            "views": self.views,
            "comments": self.get_comment_count(),
        }


class Comment(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author.username} - {self.text}"

    def get_author_avatar_url(self):
        user_info = UserInfo.objects.get(user=self.author)
        return user_info.avatar.url

    def as_dict(self):
        return {
            "pk": self.pk,
            "post_id": self.post.pk,
            "author": {
                "id": self.author.pk,
                "username": self.author.username,
                "avatar": self.get_author_avatar_url(),
            },
            "text": self.text,
            "created_date": self.created_date,
        }