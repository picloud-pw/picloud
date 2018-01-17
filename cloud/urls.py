from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    re_path(r'post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    re_path(r'post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path('auth/sign_up/', views.sign_up, name="sign_up"),
    path('auth/sign_in/', views.sign_in, name="sign_in"),
    path('auth/sign_out/', views.sign_out, name="sign_out"),
    path('search/', views.search, name="search"),
    path('memes/', views.memes, name="memes"),
    path('settings/', views.settings, name="settings"),
    path('change_password/', views.change_password, name='change_password'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('universities/', views.universities, name='universities'),

    path('get_departments/', views.get_departments, name='get_departments'),
    path('get_chairs/', views.get_chairs, name='get_chairs'),
    path('get_programs/', views.get_programs, name='get_programs'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),
]
