from django.urls import path
from hierarchy import views

app_name = 'hierarchy'

urlpatterns = [

    path('departments/', views.departments.get_all_departments,),
    path('departments/<department_id>', views.departments.get_department,),
    path('departments/<department_id>/approve', views.departments.approve_department,),
    path('departments/<department_id>/delete', views.departments.delete_department,),
    path('departments/<department_id>/subjects', views.departments.get_subjects_by_department,),

    path('subjects/', views.subjects.get_all_subjects,),
    path('subjects/<subject_id>', views.subjects.get_subject,),
    path('subjects/<subject_id>/approve', views.subjects.delete_subject,),
    path('subjects/<subject_id>/delete', views.subjects.approve_subject,),

]
