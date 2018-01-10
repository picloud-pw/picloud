from django.contrib import admin
from .models import *

admin.site.register(University)
admin.site.register(Department)
admin.site.register(Chair)
admin.site.register(Subject)
admin.site.register(Program)
admin.site.register(Lecturer)

admin.site.register(UserInfo)
admin.site.register(UserStatus)

admin.site.register(PostType)
admin.site.register(Post)
