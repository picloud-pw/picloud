from django.urls import path
from django.views.generic import RedirectView

from website.views import *

urlpatterns = [

    path('', index.index, name='index'),

    path('robots.txt', index.robots, name='robots'),
    path('about/', index.about, name='about'),
    path('legal/privacy-policy/', index.privacy_policy, name='privacy_policy'),

    path('favicon.ico/', RedirectView.as_view(url='/static/img/favicon.png', permanent=True)),
    path('favicon.png/', RedirectView.as_view(url='/static/img/favicon.png', permanent=True)),

    path('signin/', auth.sign_in, name="signin"),
    path('signout/', auth.sign_out, name="signout"),
    path('after_login/', auth.after_login, name="after_login"),

    path('cloud/', index.cloud_page, name="cloud"),

    path('posts/', index.post_page_redirect, name="posts"),
    path('posts/<int:post_id>/', index.post_page,  name="post_page"),

    path('chats/', index.chats_page, name="chats"),

    path('departments/', index.departments_page_redirect, name="departments"),
    path('deps/', index.root_departments_page, name="root_departments_page"),
    path('deps/<int:dep_id>/', index.departments_page, name="departments_page"),

    path('subjects/', index.redirect_subject_page, name="subjects"),
    path('subs/<int:sub_id>/', index.subject_page, name="subjects_page"),

    path('students/', index.redirect_students_page, name="students"),
    path('studs/', index.root_students_page, name="root_students_page"),
    path('studs/<int:stud_id>/', index.students_page, name="students_page"),

    path('moderation/', index.moderation_page, name="moderation"),
    path('memes/', index.memes_page, name="memes"),
    path('tools/', index.tools_page, name="tools"),
    path('tools/text', index.tools_text_page, name="tools_text"),

    path('new/post', index.new_post_page, name="new_post"),

    path('profile/<str:username>/', index.profile_page, name="profile"),
    path('settings/', index.settings_page, name="settings"),

]
