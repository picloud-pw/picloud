from django import forms
from .models import *
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'subject', 'type', 'image', 'link', 'file')


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', )


class SigninForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', )


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('avatar', 'program', 'course')


class AvatarChangeForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('avatar',)


class ChooseUniversityForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('university',)


class ChooseDepartmentForm(forms.ModelForm):

    class Meta:
        model = Chair
        fields = ('department',)


class ChooseChairForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('chair',)


class ChooseProgramForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('program',)


class ChooseSubjectForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('subject', 'type',)


SUBJECT_CHOICES = (
    ('Предложение по улучшению портала', 'Предложение по улучшению портала'),
    ('Жалоба', 'Жалоба'),
    ('Отзыв', 'Отзыв'),
    ('БАГ', 'БАГ'),
    ('Проблема авторизации', 'Проблема авторизациии'),
    ('Нарушение авторских прав', 'Нарушение авторских прав'),
    ('Предложение сотрудничества', 'Предложение соотрудничества'),
    ('Другое', 'Другое'),
)


class ContactForm(forms.Form):
    contact_name = forms.CharField(label="Ваше имя", required=True)
    contact_email = forms.EmailField(label="Ваш email", required=True)
    subject = forms.ChoiceField(
        label="Тема обращения",
        required=True,
        choices=SUBJECT_CHOICES,
    )
    content = forms.CharField(
        label="Сообщение",
        required=True,
        widget=forms.Textarea(attrs={'style': 'width: 100%; height:150px; resize: none'})
    )
