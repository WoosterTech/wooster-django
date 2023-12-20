# from collections.abc import Iterable
from datetime import datetime as dt
from datetime import timedelta

from basemodels.models import BaseModel, DocumentNumber
from django.db import models
from django.db.models import F, Max, Sum
from django.utils.translation import gettext_lazy as _

# from wooster_django.customers.models import Customer
# from wooster_django.inventory.models import Item
# from wooster_django.projects.models import Project
from slugify import slugify

# from wooster_django.projects.models import DocumentNumber


# Create your models here.
class Order(BaseModel):
    name = None
    number = models.CharField(_("Order Number"), max_length=50, unique=True, editable=False)
    customer = models.ForeignKey("customers.Customer", verbose_name=_("Customer"), on_delete=models.PROTECT, null=True)
    expected_date = models.DateField(_("Expected Completion Date"), auto_now=False, auto_now_add=False)
    items = models.ManyToManyField("inventory.Item", verbose_name=_("items"), through="OrderItem")
    notes = models.TextField(_("order notes"), blank=True)

    def __str__(self):
        return f"{self.customer} - {dt.strftime(self.created_date, '%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_number()
        if not self.slug:
            self.slug = slugify(self.number)
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        subtotal = (
            OrderItem.objects.filter(order=self)
            .aggregate(subtotal=Sum(F("quantity") * F("item_price"), output_field=models.DecimalField()))
            .get("subtotal")
        )
        return f"${subtotal:.2f}"

    def generate_number(self):
        order_number, _ = DocumentNumber.objects.get_or_create(
            document="Order", defaults={"prefix": "MHC", "padding_digits": 4}
        )
        return order_number.get_next_number()


class OrderItem(models.Model):
    rank = models.SmallIntegerField(_("rank"), editable=False)
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Item", verbose_name=_("Item"), on_delete=models.PROTECT)
    notes = models.TextField(_("notes"), blank=True)
    quantity = models.FloatField(_("quantity"))
    item_price = models.DecimalField(_("Item Price"), max_digits=5, decimal_places=2)

    @property
    def extended_price(self):
        return f"${self.quantity * float(self.item_price):.2f}"

    def __str__(self) -> str:
        return f"{self.order}_{self.item}_rank-{self.rank}"

    def save(self, *args, **kwargs):
        if not self.rank:
            self.rank = OrderItem.objects.filter(order=self.order).aggregate(Max("rank")) + 1
        super().save(*args, **kwargs)


def generate_empty_order():
    return Order.objects.create(expected_date=dt.today() + timedelta(days=10))
