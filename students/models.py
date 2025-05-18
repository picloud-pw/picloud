from django.contrib.auth.models import User
from django.db import models

from hierarchy.models import Department


class StudentStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)
    can_publish_without_moderation = models.BooleanField(default=False, null=False)
    can_moderate = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'level': self.status_level,
            'can_publish_without_moderation': self.can_publish_without_moderation,
            'can_moderate': self.can_moderate,
        }


class StudentInfo(models.Model):
    avatar_url = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    karma = models.SmallIntegerField(default=10, null=False)
    course = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_default_avatar_url(self, seed=None):
        if seed is None:
            seed = self.user.username
        return f"https://api.dicebear.com/5.x/bottts-neutral/svg?seed={seed}"

    def calculate_karma(self):
        from posts.models import Post, Comment

        karma = 0

        if self.department is not None:
            karma += 50
        if self.course is not None:
            karma += 30
        if self.avatar_url is not None:
            karma += 50

        karma += 15 * Post.objects.filter(author=self.user).count()
        karma += 5 * Comment.objects.filter(author=self.user).count()

        return karma

    def as_dict(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'last_login': self.user.last_login,
                'date_joined': self.user.date_joined,
            },
            'avatar': self.avatar_url if self.avatar_url is not None else self.get_default_avatar_url(),
            'status': self.status.as_dict(),
            'karma': self.calculate_karma(),
            'course': self.course,
            'department': self.department.as_dict() if self.department is not None else None,
        }
