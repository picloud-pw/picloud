from django.urls import path

from posts.views import *

app_name = 'posts'

urlpatterns = [

    path('new', posts.new, ),
    path('search', posts.search, ),

    path('get', posts.get, ),
    path('edit', posts.edit, ),
    path('delete', posts.delete, ),
    path('approve', posts.approve, ),

    path('types/get', types.get, ),

    path('comments/get', comments.get, ),
    path('comments/add', comments.add, ),
    path('comments/delete', comments.delete, ),

]
