from django.contrib import admin
from chats.models import *


admin.site.register(Chat)
admin.site.register(UserChatSettings)
admin.site.register(Message)
