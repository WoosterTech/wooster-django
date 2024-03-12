from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from slugify import slugify


# Create your models here.
class ReceiptBaseModel(models.Model):
    """Base model for standardization. Includes generating slug."""

    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("created by"), on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, editable=False)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Merchant(ReceiptBaseModel):
    def get_absolute_url(self):
        return reverse("receipts:detail_merchant", kwargs={"slug": self.slug})


class Receipt(ReceiptBaseModel):
    name = None  # type:ignore
    merchant = models.ForeignKey(Merchant, verbose_name=_("Merchant"), on_delete=models.PROTECT, null=True)
    transaction_date = models.DateField(_("Transaction Date"), auto_now=False, auto_now_add=False, null=True)
    receipt_file = models.FileField(_("Receipt"), upload_to="uploads", max_length=100)
    analyze_result = models.JSONField(_("Analyze Result"), null=True)
    slug = models.UUIDField(_("slug"), auto_created=True)


class ReceiptItem(models.Model):
    product_code = models.CharField(_("Product Code"), max_length=50)
    description = models.CharField(_("Description"), max_length=100)
    quantity = models.DecimalField(_("Quantity"), max_digits=5, decimal_places=2, default=1.0)
    total_price = models.DecimalField(_("Total Price"), max_digits=5, decimal_places=2)
    tax_code = models.CharField(_("Tax Code"), max_length=5, blank=True)
    taxable_status = models.BooleanField(_("Taxable Status"))
    receipt: models.ForeignKey = models.ForeignKey(Receipt, verbose_name=_("Receipt"), on_delete=models.CASCADE)
