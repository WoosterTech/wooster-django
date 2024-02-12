import shortuuid
from basemodels.models import BaseModel
from colorfield.fields import ColorField  # type:ignore

# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify

# from wooster_django.projects.models import BasalModel

# Chosen from https://htmlcolorcodes.com/color-names
COMMON_COLOR_PALETTE = [
    ("#FFFFFF", "white"),
    ("#000000", "black"),
    ("#FF0000", "red"),
    ("#FFC0CB", "pink"),
    ("#FFA500", "orange"),
    ("#FFFF00", "yellow"),
    ("#800080", "purple"),
    ("#008000", "green"),
    ("#0000FF", "blue"),
    ("#A52A2A", "brown"),
    ("#808080", "gray"),
]


# Create your models here.
# class BaseModel(models.Model):
#     """Base model for standardization. Includes generating slug."""

#     name = models.CharField(max_length=50)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("created by"), on_delete=models.PROTECT)
#     slug = models.SlugField(unique=True, editable=False)
#     created_date = models.DateTimeField(_("created date"), auto_now_add=True)
#     modified_date = models.DateTimeField(_("modified date"), auto_now=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)


class ItemCategory(BaseModel):
    class Meta:
        verbose_name_plural = _("item categories")
        ordering = ["name"]


class Vendor(BaseModel):
    website = models.URLField(_("website"), max_length=200, blank=True)
    contact_email = models.EmailField(_("contact email"), max_length=254, blank=True)

    class Meta:
        ordering = ["name"]


class Manufacturer(BaseModel):
    website = models.URLField(_("website"), max_length=200, blank=True)
    contact_email = models.EmailField(_("contact email"), max_length=254, blank=True)
    vendors = models.ManyToManyField("inventory.Vendor", verbose_name=_("vendor(s)"))

    class Meta:
        ordering = ["name"]


class Unit(models.Model):
    id = models.CharField(_("unit"), max_length=50, primary_key=True)
    abbreviation = models.CharField(
        _("standard abbreviation"),
        help_text=_("leave blank if no standard abbreviation"),
        max_length=50,
        blank=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.id


class Item(BaseModel):
    name = models.CharField(_("name"), max_length=100)
    internal_identifier = models.CharField(_("internal identifier"), max_length=50, blank=True)
    vendor_identifier = models.CharField(_("vendor identifier/part number/etc."), max_length=50, blank=True)
    item_categories = models.ManyToManyField("inventory.ItemCategory", verbose_name=_("item categories"))
    manufacturer = models.ForeignKey(
        "inventory.Manufacturer",
        verbose_name=_("primary manufacturer"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="primary_manufacturer",
    )
    alternate_manufacturers = models.ManyToManyField(
        "inventory.Manufacturer",
        verbose_name=_("alternate manufacturers"),
        related_name="alt_manufacturers",
        blank=True,
    )
    vendor = models.ForeignKey(
        "inventory.Vendor",
        verbose_name=_("Primary Vendor"),
        on_delete=models.PROTECT,
        related_name="primary_vendor",
        null=True,
    )
    alternate_vendors = models.ManyToManyField(
        "inventory.Vendor", verbose_name=_("alternate vendors"), related_name="alt_vendors", blank=True
    )
    common_color = ColorField(choices=COMMON_COLOR_PALETTE, blank=True)
    true_color = ColorField(samples=COMMON_COLOR_PALETTE, blank=True)
    size = models.CharField(_("size"), help_text=_("e.g. small/medium/large or '32 oz.'"), max_length=50, blank=True)
    is_sellable = models.BooleanField(_("can be sold"))
    is_raw_material = models.BooleanField(_("raw material"))
    is_parent_item = models.BooleanField(
        _("parent item"),
        help_text="use for items that can have multiple variations; e.g. '32 oz. Thermoflask', each color/item number will then have their own items",  # noqa: E501
    )
    parent_item = models.ForeignKey(
        "self", verbose_name=_("parent item"), on_delete=models.PROTECT, null=True, blank=True
    )
    # in_stock_quantity = models.IntegerField(_("quantity in stock"), default=0)
    in_stock_amount = models.DecimalField(_("amount in stock"), max_digits=5, decimal_places=2, default=0.0)
    in_stock_amount_unit = models.ForeignKey("inventory.Unit", verbose_name=_("Stock Unit"), on_delete=models.PROTECT)

    class Meta:
        ordering = ["manufacturer", "is_parent_item", "name"]


class History(BaseModel):
    name = None
    item = models.ForeignKey("inventory.Item", verbose_name=_("item"), on_delete=models.CASCADE)
    amount = models.DecimalField(_("amount"), help_text=_("always >= 0"), max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-created_date"]
        verbose_name_plural = _("histories")

    class HistoryType(models.TextChoices):
        ADD = "add", _("Add")
        SUBTRACT = "subtract", _("Subtract")
        CORRECT = "correct", _("Correct")
        INITIAL = "initial", _("Initial")

    history_type = models.CharField(
        _("history type"), max_length=10, choices=HistoryType.choices, default=HistoryType.SUBTRACT
    )

    def __str__(self):
        return f"{self.item} | {self.created_date}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            EditItem = self.item
            if self.history_type == self.HistoryType.ADD:
                EditItem.in_stock_amount += self.amount
            elif self.history_type == self.HistoryType.SUBTRACT:
                EditItem.in_stock_amount -= self.amount
            elif self.history_type == self.HistoryType.CORRECT or self.history_type == self.HistoryType.INITIAL:
                EditItem.in_stock_amount = self.amount
            else:
                raise Exception("Invalid history type")

            EditItem.save()

            slug = shortuuid.uuid()[:10]
            self.slug = slugify(slug)
        return super().save(*args, **kwargs)
