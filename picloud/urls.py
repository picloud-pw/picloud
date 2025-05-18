from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import website.views

handler404 = website.views.errors.handler404
handler500 = website.views.errors.handler500


urlpatterns = [

    path('', include('social_django.urls', namespace='social')),
    path('', include('website.urls')),

    path('admin/', admin.site.urls, name='admin'),
    path('hierarchy/', include('hierarchy.urls', namespace='hierarchy')),
    path('memes/', include('memes.urls', namespace='memes')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('students/', include('students.urls', namespace='students')),
    path('chats/', include('chats.urls', namespace='chats')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
