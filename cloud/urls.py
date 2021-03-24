from django.urls import path

from cloud import legacy_views

urlpatterns = [

    path('user/<user_id>', legacy_views.user_page),
    path('user/<user_id>/posts', legacy_views.user_posts),
    path('user/<user_id>/not_checked_posts', legacy_views.user_not_checked_posts),

    path('settings/', legacy_views.settings_page),
    path('auth/signin/', legacy_views.auth_signin),
    path('feed/', legacy_views.feed_page),

    path('universities/', legacy_views.universities_list),
    path('universities/<university_id>/', legacy_views.university_page),
    path('universities/<university_id>/students', legacy_views.students_from_university),
    path('programs/<program_id>', legacy_views.program_page),
    path('subjects/<subject_id>', legacy_views.subject_page),

    path('post/<post_id>/', legacy_views.post_page_redirect),

]
