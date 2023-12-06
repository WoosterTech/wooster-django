from django.contrib import admin

from .models import History, Item, ItemCategory, Manufacturer, Unit, Vendor

# from django.http.request import HttpRequest
# from django.conf import settings
# from django.apps import AppConfig


# Register your models here.
class ItemCategoriesInline(admin.TabularInline):
    model = Item.item_categories.through
    exclude = ["created_by", "created_date"]
    extra = 0


class ItemInline(admin.TabularInline):
    model = Item
    exclude = ["created_by"]
    extra = 0


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [ItemCategoriesInline]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "website", "contact_email"]
    search_fields = ["name"]
    inlines = [ItemInline]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "website", "contact_email"]
    search_fields = ["name"]
    inlines = [ItemInline]


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


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["created_date", "item", "amount", "history_type"]
    search_fields = ["item"]
    list_filter = ["history_type"]
    date_hierarchy = "created_date"
    # list_display_links = ["created_date", "item"]

    # def get_changeform_initial_data(self, request: HttpRequest) -> dict[str, str]:
    #     UserModel = AppConfig.get_model("User")
    #     RequestUser = UserModel.get(email=request.user)
    #     return {"created_by", RequestUser}
