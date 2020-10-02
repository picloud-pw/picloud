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

    path('cloud/', index.cloud_page, name="cloud"),
    path('moderation/', index.moderation_page, name="moderation"),

]
