from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    path(r'post/new/', views.post_new, name='post_new'),
    path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]