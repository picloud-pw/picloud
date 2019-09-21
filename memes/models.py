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
