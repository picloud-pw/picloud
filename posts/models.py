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

    def html(self):
        dangerous_html = markdown.markdown(self.text, extensions=['markdown.extensions.fenced_code'])
        safe_html = bleach.clean(dangerous_html, tags=self.ALLOWED_HTML_TAGS)
        html_with_hyperlinks = bleach.linkify(safe_html)
        return html_with_hyperlinks

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

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

    def as_dict(self):
        return {
            "id": self.pk,
            "author_username": self.author.username,
            "author_id": self.author.pk,
            "title": self.title,
            "text": self.text,
            "created_date": self.created_date,
            "subject_id": self.subject.pk,
            "subject_short_title": self.subject.short_title,
            "type_title": self.type.title,
            "link": self.link,
            "views": self.views,
            "image": self.get_image_url(),
            "file": self.get_file_url(),
        }

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
            "author_id": self.author.pk,
            "author_username": self.author.username,
            "author_avatar": self.get_author_avatar_url(),
            "text": self.text,
            "created_date": self.created_date,
        }