from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Chat(models.Model):
    author = models.ForeignKey(User, related_name='author', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=128)
    name = models.CharField(max_length=32, unique=True)
    members = models.ManyToManyField(User, related_name='members')

    def as_dict(self):
        return {
            'author': self.author.username if self.author is not None else None,
            'created': self.created,
            'title': self.title,
            'name': self.name,
            'members_count': self.members.all().count(),
        }


class UserChatSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    muted = models.BooleanField(default=False)

    def as_dict(self):
        return {
            'muted': self.muted,
        }


class Message(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(null=True, blank=True)

    def as_dict(self):
        return {
            'author': self.author.username if self.author is not None else None,
            'text': self.text,
            'created': self.created,
            'edited': self.edited if self.edited is not None else None,
        }
