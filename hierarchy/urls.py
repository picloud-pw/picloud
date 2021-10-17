from django.urls import path
from hierarchy import views

app_name = 'hierarchy'

urlpatterns = [

    path('cities/search', views.sities.search_cities),

    path('universities/search', views.universities.search_universities),
    path('universities/add', views.universities.add_university,),

    path('departments/types', views.departments.get_department_types,),
    path('departments/search', views.departments.search_departments,),
    path('departments/get', views.departments.get_department,),

    path('subjects/search', views.subjects.search_subjects, ),
    path('subjects/get', views.subjects.get_subject, ),

]
