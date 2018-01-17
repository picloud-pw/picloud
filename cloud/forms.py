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
        fields = ('subject',)