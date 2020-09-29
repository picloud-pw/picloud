from django.urls import path

from posts.views import *

app_name = 'posts'

urlpatterns = [

    path('new', posts.new, ),
    path('search', posts.search, ),

    path('<int:post_id>/', posts.get, ),
    path('<int:post_id>/edit/', posts.edit, ),
    path('<int:post_id>/delete/', posts.delete, ),
    path('<int:post_id>/approve/', posts.approve, ),

    path('<int:post_id>/comments/', comments.get, ),
    path('<int:post_id>/comments/add', comments.add, ),
    path('<int:post_id>/comments/<int:comment_id>/delete', comments.delete, ),

]
