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


class UserInfoChangeForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('program', 'course')


class UserNameChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


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


SORT_TYPE = (
    ('newest', 'По дате (сначала новые)'),
    ('oldest', 'По дате (сначала старые)'),
    ('last_semester', 'По семестру (сначала старшие)'),
    ('first_semester', 'По семестру (сначала младшие)'),
    ('most_views', 'По просмотрам (по убыванию)'),
    ('least_views', 'По просмотрам (по возрастанию)'),
)


class ChooseSortForm(forms.Form):
    sort_type = forms.ChoiceField(
        label="Сортировка",
        required=True,
        choices=SORT_TYPE,
    )


SUBJECT_CHOICES = (
    ('Предложение по улучшению портала', 'Предложение по улучшению портала'),
    ('Жалоба', 'Жалоба'),
    ('Отзыв', 'Отзыв'),
    ('Баг', 'Баг'),
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


class NewUniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ('title', 'short_title', 'link', 'logo', )


class NewDepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('university', 'title', 'short_title', 'link', )


class NewChairForm(forms.ModelForm):

    class Meta:
        model = Chair
        fields = ('department', 'title', 'short_title', 'link', )


class NewProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('chair', 'title', 'code', 'link', )


class NewSubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ('programs', 'title', 'short_title', 'semester',)
