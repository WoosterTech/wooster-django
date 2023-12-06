from django.contrib import admin
from projects.models import Project

from .models import Customer


# Register your models here.
class ProjectInline(admin.TabularInline):
    model = Project
    exclude = ["created_by"]
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["organization_name", "contact_name", "contact_email"]
    search_fields = ["organization_name", "contact_name", "contact_email"]
    inlines = [ProjectInline]
