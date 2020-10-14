from django.urls import path

from .views import *

app_name = 'students'

urlpatterns = [

    path('me/', me,),
    path('me/edit', me_edit,),

    path('search', search,),

]
