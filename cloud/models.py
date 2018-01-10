from django.db import models
from django.utils import timezone


class PostType(models.Model):
    title = models.CharField(max_length=256, null=False, unique=True)

    def __str__(self):
        return self.title


class University(models.Model):
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    logo = models.ImageField(upload_to='resources/u_logo/', null=True, blank=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.title


class Chair(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.title


class Lecturer(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, null=True, blank=True)
    complexity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='resources/lec_avatars/', null=True, blank=True)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic


class Subject(models.Model):
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=16, null=True, blank=True)
    course = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.short_title + " (" + self.title + ")"


class Program(models.Model):
    chair = models.ForeignKey('Chair', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    code = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.title


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    avatar = models.ImageField(upload_to='resources/user_avatars/', null=True, blank=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    status = models.ForeignKey('UserStatus', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, null=True, blank=True)
    karma = models.SmallIntegerField(default=10, null=False)


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    type = models.ForeignKey('PostType', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    validate_status = models.PositiveSmallIntegerField(default=0)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
