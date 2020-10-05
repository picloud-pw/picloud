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
    path('departments/', index.departments_page, name="departments"),
    path('moderation/', index.moderation_page, name="moderation"),

]
