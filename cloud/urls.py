from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from cloud import views

urlpatterns = [

    path('auth/delete-me/', views.user.delete_active_account, name='account_delete_active'),

    path('user/<user_id>', views.user.user_page, name='user_page'),
    path('user/<user_id>/posts', views.user.user_posts, name='user_posts'),
    path('user/<user_id>/karma', views.karma.info_page, name="karma_info_page"),
    path('user/<user_id>/not_checked_posts', views.user.user_not_checked_posts, name='user_not_checked_posts'),

    path('search/', views.search.text_search, name='search'),
    path('settings/', views.user.settings_page, name="settings"),
    path('message/', views.message.message, name="message"),
    path('moderation/update_karma', views.karma.update_karma_for_all_users, name="update_karma"),
    path('change_password/', views.user.change_password, name='change_password'),
    path('change_avatar/', views.user.change_avatar, name='change_avatar'),
    path('change_user/', views.user.change_user, name='change_user'),
    path('change_user_name/', views.user.change_user_name, name='change_user_name'),

    path('universities/', views.universities.universities_list, name='universities_list'),
    path('universities/<university_id>/', views.universities.university_page, name='university_page'),
    path('universities/<university_id>/students', views.universities.students_from_university, name='stud_from_univ'),
    path('universities/<university_id>/delete', views.universities.university_delete, name='university_delete'),
    path('universities/<university_id>/approve', views.universities.university_approve, name='university_approve'),

    path('departments/<department_id>/approve', views.departments.department_approve, name='department_approve'),
    path('departments/<department_id>/delete', views.departments.department_delete, name='department_delete'),

    path('chairs/<chair_id>/approve', views.chairs.chair_approve, name='chair_approve'),
    path('chairs/<chair_id>/delete', views.chairs.chair_delete, name='chair_delete'),

    path('programs/<program_id>', views.programs.program_page, name='program_page'),
    path('programs/<program_id>/approve', views.programs.program_approve, name='program_approve'),
    path('programs/<program_id>/delete', views.programs.program_delete, name='program_delete'),

    path('subjects/<subject_id>', views.subjects.subject_page, name='subject_page'),
    path('subjects/<subject_id>/approve', views.subjects.subject_approve, name='subject_approve'),
    path('subjects/<subject_id>/delete', views.subjects.subject_delete, name='subject_delete'),

    path('memes/', views.memes.get_memes, name='memes'),

    path('submit/university/', views.universities.new_university, name='new_university'),
    path('submit/department/', views.departments.new_department, name='new_department'),
    path('submit/chair/', views.chairs.new_chair, name='new_chair'),
    path('submit/program/', views.programs.new_program, name='new_program'),
    path('submit/subject/', views.subjects.new_subject, name='new_subject'),

    # TODO: Сделать похожим на RESTful
    path('api/hierarchy/', views.structure.hierarchy_dump, name='get_structure_hierarchy'),
    path('api/universities/', views.api.get_universities, name='get_universities'),
    path('api/departments/', views.api.get_departments, name='get_departments'),
    path('api/chairs/', views.api.get_chairs, name='get_chairs'),
    path('api/programs/', views.api.get_programs, name='get_programs'),
    path('api/subjects/', views.api.get_subjects, name='get_subjects'),
    path('api/posts/', views.search.search_and_render_posts, name='get_posts'),
    path('api/search_posts/', views.search.search_posts, name='search_posts'),
]
