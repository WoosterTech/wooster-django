from django.contrib import admin

# from inventory.models import Item
from wooster_django.projects.models import Project

from .models import DocumentNumber, Invoice, InvoiceLine, Order, OrderItem


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


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    readonly_fields = ["rank", "extended_price"]
    fields = ["rank", "description", "quantity", "unit_price", "extended_price"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["number", "customer", "status"]
    list_filter = ["customer"]
    date_hierarchy = "created"
    search_fields = ["number", "customer"]
    readonly_fields = ["status_changed"]
    inlines = [InvoiceLineInline]


@admin.register(DocumentNumber)
class DocumentNumberAdmin(admin.ModelAdmin):
    list_display = ["document", "last_number"]
    search_fields = ["document"]
    readonly_fields = ["last_number", "last_generated_date"]
