from django.db import models
from social.tests.models import User


class MemeSource(models.Model):
    source = models.URLField(null=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.source
