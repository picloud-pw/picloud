from django.contrib import admin

from posts.models import *


admin.site.register(PostType)
admin.site.register(Post)
admin.site.register(Attachment)
admin.site.register(Comment)
