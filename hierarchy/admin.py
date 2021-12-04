from django.contrib import admin
from hierarchy.models import *


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_type', 'name', 'vk_id')
    search_fields = ['name']

    list_filter = (
        ('department_type__name', admin.AllValuesFieldListFilter),
    )


admin.site.register(DepartmentType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Subject)
