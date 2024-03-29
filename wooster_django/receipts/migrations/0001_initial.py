# Generated by Django 4.2.7 on 2024-02-12 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Merchant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(editable=False, unique=True)),
                ("created_date", models.DateTimeField(auto_now_add=True, verbose_name="created date")),
                ("modified_date", models.DateTimeField(auto_now=True, verbose_name="modified date")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Receipt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.UUIDField(auto_created=True, verbose_name="slug")),
                ("created_date", models.DateTimeField(auto_now_add=True, verbose_name="created date")),
                ("modified_date", models.DateTimeField(auto_now=True, verbose_name="modified date")),
                ("transaction_date", models.DateField(verbose_name="Transaction Date")),
                ("receipt_file", models.FileField(upload_to="uploads", verbose_name="Receipt")),
                ("analyze_result", models.JSONField(verbose_name="Analyze Result")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="receipts.merchant", verbose_name="Merchant"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReceiptItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_code", models.CharField(max_length=50, verbose_name="Product Code")),
                ("description", models.CharField(max_length=100, verbose_name="Description")),
                (
                    "quantity",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=5, verbose_name="Quantity"),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Total Price")),
                ("tax_code", models.CharField(blank=True, max_length=5, verbose_name="Tax Code")),
                ("taxable_status", models.BooleanField(verbose_name="Taxable Status")),
                (
                    "receipt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="receipts.receipt", verbose_name="Receipt"
                    ),
                ),
            ],
        ),
    ]
