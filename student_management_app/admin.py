from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser, SubjectDescriptionFile


class UserModel(UserAdmin):
    pass


class SubjectDescriptionFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'file_name', 'uploaded_at']
    list_filter = ['subject', 'uploaded_at']
    search_fields = ['file_name', 'subject__subject_name']
    ordering = ['-uploaded_at']


admin.site.register(CustomUser, UserModel)
admin.site.register(SubjectDescriptionFile, SubjectDescriptionFileAdmin)
