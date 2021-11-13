from django.urls import path

from chats.views import *

app_name = 'chats'


urlpatterns = [
    path('chat/list', chat_list, ),
    path('chat/add', chat_add, ),
    path('chat/delete', chat_delete, ),

    path('message/list', message_list, ),
    path('message/add', message_add),
    path('message/edit', message_edit),
    path('message/delete', message_delete),
]
