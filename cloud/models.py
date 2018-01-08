from django.db import models
from django.utils import timezone

'''
class University(models.Model):
    title = models.CharField(max_length=256, null=False)
    #logo = models.ImageField(upload_to='resources/u_logo/')

    def __str__(self):
        return self.title


class Department(models.Model):
    university = models.ForeignKey("University", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.title


class Chair(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.title


class Program(models.Model):
    chair = models.ForeignKey("Chair", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    start_year = models.DateField(auto_now=False, auto_now_add=False, null=False)

    def __str__(self):
        return self.title


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    status = models.ForeignKey('UserStatus', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    karma = models.SmallIntegerField(default=10, null=False)


class Lecturer(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    complexity = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Subject(models.Model):
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=16, null=False)
    course = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.short_title + " (" + self.title+ ")"


class PostType(models.Model):
    title = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.title

'''
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    # subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)
    # type = models.ForeignKey('PostType', on_delete=models.CASCADE, null=True)
    # image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True)
    # link = models.URLField(max_length=512, null=True)
    # file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True)
    # validate_status = models.PositiveSmallIntegerField(default=0)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title