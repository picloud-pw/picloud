from django.contrib.auth.models import User
from django.db import models

from hierarchy.models import Department


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)
    can_publish_without_moderation = models.BooleanField(default=False, null=False)
    can_moderate = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'title': self.title,
            'level': self.status_level,
            'can_publish_without_moderation': self.can_publish_without_moderation,
            'can_moderate': self.can_moderate,
        }


class UserInfo(models.Model):
    avatar = models.ImageField(
        upload_to='resources/user_avatars/',
        default='resources/default/user_ava.png',
        null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(UserStatus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    karma = models.SmallIntegerField(default=10, null=False)
    course = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def as_dict(self):
        return {
            'user': {
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'last_login': self.user.last_login,
                'date_joined': self.user.date_joined,
            },
            'avatar': self.avatar.url,
            'status': self.status.as_dict(),
            'karma': self.karma,
            'course': self.course,
            'department': self.department.as_dict() if self.department is not None else None,
        }
