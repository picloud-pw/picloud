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
    path('universities/', views.universities, name='universities'),
]
