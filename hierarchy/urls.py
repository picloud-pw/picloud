from django.urls import path
from hierarchy import views

app_name = 'hierarchy'

urlpatterns = [

    path('departments/search', views.departments.search_departments,),

    path('subjects/search', views.subjects.search_subjects, ),

]
