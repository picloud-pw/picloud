from django.contrib import admin

from posts.models import *

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'link')
    search_fields = ['title', 'id']
    ordering = ['-created_date']

admin.site.register(PostType)
admin.site.register(Post, PostsAdmin)
admin.site.register(Comment)
