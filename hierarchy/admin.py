from django.contrib import admin
from hierarchy.models import *


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(DepartmentType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Subject)
