from django.urls import path

from .views import *

app_name = 'students'

urlpatterns = [

    path('me/', me,),
    path('me/edit', me_edit,),
    path('me/avatar/delete', delete_avatar,),
    path('me/avatar/set_default', avatar_set_default,),

    path('get', get,),
    path('search', search,),

    path('statuses', get_statuses)

]
