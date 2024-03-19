# Generated by Django 4.2.7 on 2024-03-13 07:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields
from wooster_django.orders.models import NumberField
# import orders.models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0001_initial"),
        ("orders", "0008_rename_documentnumbers_documentnumber"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "status_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now, monitor="status", verbose_name="status changed"
                    ),
                ),
                (
                    "number",
                    NumberField(
                        document_type="Invoice", padding=4, prefix="INV-", start_index=1000, verbose_name="number"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "draft"),
                            ("estimate", "estimate"),
                            ("invoiced", "invoiced"),
                            ("paid", "paid"),
                        ],
                        default="draft",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                ("terms", models.TextField(verbose_name="terms")),
                ("notes", models.TextField(verbose_name="notes")),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from="number"),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="customers.customer", verbose_name="customer"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
