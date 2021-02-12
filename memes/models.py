from django.contrib.auth.models import User
from django.db import models

from hierarchy.models import Department


class MemesSource(models.Model):
    source = models.URLField(null=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.source

    def as_dict(self):
        return {
            'id': self.id,
            'source': self.source,
            'author': None if self.author is None else {
                'user_id': self.author.id,
                'username': self.author.username,
            },
            'department': self.department.as_dict() if self.department is not None else None,
            'is_public': self.is_public,
            'is_approved': self.is_approved
        }
