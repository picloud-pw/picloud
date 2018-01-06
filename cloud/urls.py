from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    path(r'post/new/', views.post_new, name='post_new'),
    path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path(r'^auth/sign_up/', views.sign_up, name="sign_up"),
    path(r'^auth/sign_in/', views.sign_in, name="sign_in"),
    path(r'^auth/sign_out/', views.sign_out, name="sign_out"),
    path(r'^search/', views.search, name="search"),
    path(r'^memes/', views.memes, name="memes"),
]