# from collections.abc import Iterable
import logging
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
from decimal import Decimal
from typing import Any

from basemodels.models import BaseModel
from django.conf import settings
from django.db import models
from django.db.models import Count, F, Max, Sum
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

# from wooster_django.customers.models import Customer
# from wooster_django.inventory.models import Item
# from wooster_django.projects.models import Project
from slugify import slugify

# from wooster_django.projects.models import DocumentNumbers  # , BasalModel


# Create your models here.

logger = logging.getLogger(__name__)
if settings.DEBUG:
    logger.setLevel(logging.DEBUG)


class DocumentNumber(models.Model):
    document = models.CharField(max_length=50, primary_key=True, unique=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    padding_digits = models.IntegerField(blank=True, null=True)
    next_counter = models.IntegerField(default=1)
    last_number = models.CharField(max_length=50, editable=False, null=True)
    last_generated_date = models.DateTimeField(auto_now=True)

    def get_next_number(self):
        prefix = self.prefix
        next_counter = self.next_counter
        padded_counter = str(next_counter).zfill(self.padding_digits)
        number = f"{prefix}{padded_counter}"

        self.next_counter += 1
        self.last_number = number

        self.save()

        return number

    def __str__(self) -> str:
        return f'DocumentNumber(document="{self.document}", prefix="{self.prefix}")'


class NumberField(models.CharField):
    description = "A field that auto-generates a sequential number with a prefix and padding."

    def __init__(
        self,
        document_type: str,
        prefix: str,
        step: int = 1,
        padding: int = 4,
        start_index: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.document_type = document_type
        self.prefix = prefix
        self.step = step
        self.padding = padding
        self.start_index = start_index
        self._all_attributes = ["document_type", "prefix", "step", "padding", "start_index"]
        self._with_defaults = {"step": 1, "padding": 1, "start_index": 0}

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        logger.debug("All attributes: %s", self._all_attributes)
        for attribute in self._all_attributes:
            attribute_value = getattr(self, attribute)
            if attribute in [key for key in self._with_defaults]:
                if attribute_value != self._with_defaults[attribute]:
                    kwargs[attribute] = attribute_value
                logger.debug(
                    "Attribute %(attr)s has default %(default)s"
                    % {"attr": attribute, "default": self._with_defaults[attribute]}
                )
            else:
                kwargs[attribute] = attribute_value

        return name, path, args, kwargs

    @property
    def non_db_attrs(self):
        additional_attrs = ("document_type", "prefix", "step", "padding", "start_index")
        return super().non_db_attrs + additional_attrs

    def pre_save(self, model_instance: models.Model, add: bool) -> Any:
        if add:
            number, _ = DocumentNumber.objects.get_or_create(
                document=self.document_type,
                defaults={"prefix": self.prefix, "padding_digits": self.padding, "last_number": self.start_index},
            )
            next_number = number.get_next_number()
            setattr(model_instance, self.attname, next_number)
            return next_number

        return super().pre_save(model_instance, add)


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
        return f"${subtotal:.2f}" if subtotal is not None else "$0.00"

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


def get_default_due_date():
    return date.today() + timedelta(days=30)


class Invoice(TimeStampedModel, StatusModel):
    number = NumberField(
        document_type="Invoice", prefix="INV-", verbose_name=_("number"), padding=4, start_index=1000, editable=False
    )
    STATUS = Choices(
        ("draft", _("Draft")), ("stimate", _("Estimate")), ("invoiced", _("Invoiced")), ("paid", _("Paid"))
    )
    status = models.CharField(_("status"), choices=STATUS, max_length=50, default=STATUS.draft)
    customer = models.ForeignKey("customers.Customer", verbose_name=_("customer"), on_delete=models.PROTECT)
    terms = models.TextField(_("terms"), blank=True)
    notes = models.TextField(_("notes"), blank=True)
    subtotal = models.DecimalField(_("subtotal"), max_digits=15, decimal_places=5, default=0)
    grand_total = models.DecimalField(_("grand total"), max_digits=15, decimal_places=5, default=0)
    due_date = models.DateField(_("due date"), default=get_default_due_date)
    project = models.ForeignKey(
        "projects.Project", verbose_name=_("linked project"), on_delete=models.PROTECT, null=True
    )

    slug = AutoSlugField(populate_from="number", slugify_function=slugify)

    def __str__(self):
        return f"{self.customer} - {self.number}"

    def update_totals(self) -> None:
        total = self.get_subtotal()
        kwargs = {"subtotal": total, "grand_total": total}
        self.__class__.objects.filter(pk=self.pk).update(**kwargs)

    def get_subtotal(self) -> Decimal:
        return self.invoiceline_set.aggregate(subtotal=Sum(F("quantity") * F("unit_price")))["subtotal"]

    def normalize_rank(self) -> None:
        qs: models.QuerySet[InvoiceLine]
        qs = self.invoiceline_set.order_by("rank")
        result = qs.aggregate(Count("rank"), Max("rank"))

        count, max = result["rank__count"], result["rank__max"]

        if count == max or count == 0:
            return

        # shift all ranks outside current range to prevent uniqueness errors

        qs.update(rank=F("rank") + int(max))

        # rewrite ranks starting at 1
        for (
            idx,
            line,
        ) in enumerate(qs):
            line.rank = idx + 1
        qs.bulk_update(qs, ["rank"])


# class LineItemBase(models.Models):
#     class Meta:
#         abstract = True

#     rank = models.PositiveSmallIntegerField(_("rank"))

#     def save(self, *args, **kwargs):
#         parent = self.__class__.objects.filter()
#         current_max =


class InvoiceLine(models.Model):
    rank = models.PositiveSmallIntegerField(_("rank"))
    description = models.CharField(_("description"), max_length=100)
    quantity = models.DecimalField(_("quantity"), max_digits=15, decimal_places=5, default=1)
    unit_price = models.DecimalField(_("unit price"), max_digits=15, decimal_places=4, default=0)
    invoice = models.ForeignKey(Invoice, verbose_name=_("invoice"), on_delete=models.CASCADE)

    @property
    def extended_price(self):
        return self.quantity * self.unit_price

    @property
    def line_number(self):
        return self.rank

    def __str__(self) -> str:
        return f"{self.description}|{self.invoice.number} - Line {self.rank}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.rank = self.get_next_rank()
        super().save(*args, **kwargs)

        self.invoice.update_totals()

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        deleted = super().delete(*args, **kwargs)

        self.invoice.normalize_rank()

        return deleted

    def get_next_rank(self) -> int:
        results = self.__class__.objects.filter(invoice=self.invoice).aggregate(Max("rank"))

        return results["rank__max"] + 1 if results["rank__max"] is not None else 1
