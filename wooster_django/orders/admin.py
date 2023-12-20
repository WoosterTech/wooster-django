from django.contrib import admin

# from inventory.models import Item
from projects.models import Project

from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["number", "customer", "expected_date", "subtotal"]
    list_filter = ["customer"]
    date_hierarchy = "created_date"
    search_fields = ["number", "customer"]
    inlines = [OrderItemInline, ProjectInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "extended_price"]
