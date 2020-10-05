from django.urls import path
from hierarchy import views

app_name = 'hierarchy'

urlpatterns = [

    path('departments/types', views.departments.get_department_types,),
    path('departments/search', views.departments.search_departments,),
    path('departments/get', views.departments.get_department,),

    path('subjects/search', views.subjects.search_subjects, ),

]
