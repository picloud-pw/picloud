from django.urls import path
from . import views

app_name = 'memes'

urlpatterns = [
    path('sources/', views.get_sources),
    path('memes/', views.get_memes),
]
