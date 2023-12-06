from django.contrib import admin

from .models import Item, ItemCategory, Manufacturer, Unit, Vendor


# Register your models here.
@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "website", "contact_email"]
    search_fields = ["name"]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "website", "contact_email"]
    search_fields = ["name"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["id", "abbreviation"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "internal_identifier",
        "vendor_identifier",
        "in_stock_amount",
        "in_stock_amount_unit",
        "manufacturer",
        "vendor",
        "common_color",
    ]
    list_editable = ["in_stock_amount", "in_stock_amount_unit"]
    search_fields = ["name", "internal_identifier", "vendor_identifier", "common_color"]
    filter_horizontal = ["alternate_manufacturers", "alternate_vendors", "item_categories"]
    list_filter = ["manufacturer", "vendor", "in_stock_amount_unit", "common_color"]
