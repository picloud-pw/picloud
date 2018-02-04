from django.db import models
from django.utils import timezone


class University(models.Model):
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    logo = models.ImageField(upload_to='resources/u_logo/',
                             default='resources/default/u_logo.png',
                             null=True, blank=True)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }


class Department(models.Model):
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }


class Chair(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.short_title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }


class Program(models.Model):
    chair = models.ForeignKey('Chair', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    code = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.title + " (" + self.chair.__str__() + ")"

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "code": self.code
        }


class Lecturer(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, null=True, blank=True)
    complexity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='resources/lec_avatars/',
                              default='resources/default/lec_avatar.png',
                              null=True, blank=True)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic


class Subject(models.Model):
    programs = models.ManyToManyField("Program")
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=16, null=True, blank=True)
    semestr = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.short_title + " (" + self.semestr.__str__() + " семестр)"

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "semestr": self.semestr
        }


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    avatar = models.ImageField(upload_to='resources/user_avatars/',
                               default='resources/default/user_ava.png',
                               null=True, blank=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    status = models.ForeignKey('UserStatus', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, null=True, blank=True)
    karma = models.SmallIntegerField(default=10, null=False)
    course = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class PostType(models.Model):
    title = models.CharField(max_length=256, null=False, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    type = models.ForeignKey('PostType', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    validate_status = models.PositiveSmallIntegerField(default=0)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "author_username": self.author.username,
            "author_id": self.author.pk,
            "title": self.title,
            "text": self.text,
            "create_date": self.created_date,
            "subject_id": self.subject.pk,
            "subject_short_title": self.subject.short_title,
            "type_title": self.type.title,
            "link": self.link,
            "views": self.views,
        }
