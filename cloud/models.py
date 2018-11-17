from django.db import models
from django.utils import timezone
from django.contrib import auth
import os

import bleach
import markdown


class University(models.Model):
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    logo = models.ImageField(upload_to='resources/u_logo/',
                             default='resources/default/u_logo.png',
                             null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "deparments": {
                d.id: d.as_hierarchical_dict()
                for d in Department.objects.filter(university=self.pk, is_approved=True)
            }
        }


class Department(models.Model):
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "chairs": {
                c.id: c.as_hierarchical_dict()
                for c in Chair.objects.filter(department=self.pk, is_approved=True)
            }
        }


class Chair(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.short_title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "programs": {
                p.id: p.as_hierarchical_dict()
                for p in Program.objects.filter(chair=self.pk, is_approved=True)
            }
        }


class Program(models.Model):
    chair = models.ForeignKey('Chair', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    code = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " (" + str(self.chair) + ")"

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "code": self.code
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "code": self.code,
            "subjects": {
                s.id: s.as_dict()
                for s in Subject.objects.filter(programs=self.pk, is_approved=True)
            }
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
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic


class Subject(models.Model):
    programs = models.ManyToManyField("Program")
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=16, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.displayed_title()

    def displayed_title(self):
        if self.semester != 0:
            return self.title + " (" + str(self.semester) + " сем.)"
        else:
            return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.displayed_title(),
            "short_title": self.short_title,
            "semester": self.semester
        }


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)
    can_publish_without_moderation = models.BooleanField(default=False, null=False)
    can_moderate = models.BooleanField(default=False, null=False)

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
    vk_id = models.CharField(max_length=16, null=True, default=None)

    def __str__(self):
        return self.user.username


class MemeSource(models.Model):
    link = models.URLField(null=False, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    chair = models.ForeignKey('Chair', on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.link


class PostType(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=256, null=False, unique=True)
    plural = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    parent_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    last_editor = models.ForeignKey('auth.User', related_name='last_editor', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    type = models.ForeignKey('PostType', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    ALLOWED_HTML_TAGS = allowed_html_tags = bleach.ALLOWED_TAGS + [
        u'h1',
        u'h2',
        u'h3',
        u'h4',
        u'p',
        u'a',
        u'li',
        u'ul',
        u'ol',
        u'pre',
        u'code',
        u'hr',
        u'br',
        u'strong',
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
