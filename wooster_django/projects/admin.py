from django.contrib import admin

from .models import Project

# Register your models here.
# @admin.register(DocumentNumbers)
# class DocumentNumberAdmin(admin.ModelAdmin):
#     list_display = ["document", "last_number", "next_counter"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_number", "customer", "name"]
    list_filter = ["customer"]
    date_hierarchy = "created_date"
    search_fields = ["project_number", "customer", "name"]
