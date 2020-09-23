from django.urls import path
from hierarchy import views


urlpatterns = [

    path('departments/', views.departments.get_all_departments, name='get_all_departments'),
    path('departments/<department_id>', views.departments.get_department, name='get_department'),
    path('departments/<department_id>/approve', views.departments.approve_department, name='approve_department'),
    path('departments/<department_id>/delete', views.departments.delete_department, name='delete_department'),
    path('departments/<department_id>/subjects',
         views.departments.get_subjects_by_department,
         name='get_subjects_by_department'
         ),

    path('subjects/', views.subjects.get_all_subjects, name='get_all_subjects'),
    path('subjects/<subject_id>', views.subjects.get_subject, name='get_subject'),
    path('subjects/<subject_id>/approve', views.subjects.delete_subject, name='delete_subject'),
    path('subjects/<subject_id>/delete', views.subjects.approve_subject, name='approve_subject'),

]
