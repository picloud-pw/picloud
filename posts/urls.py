from django.urls import path

from posts.views import *

app_name = 'posts'

urlpatterns = [

    path('create', posts.create, ),
    path('search', posts.search, ),

    path('get', posts.get, ),
    path('update', posts.update, ),
    path('submit', posts.submit, ),
    path('delete', posts.delete, ),
    path('approve', posts.approve, ),

    path('types/get', types.get, ),

    path('comments/get', comments.get, ),
    path('comments/add', comments.add, ),
    path('comments/delete', comments.delete, ),

]
