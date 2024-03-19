# Generated by Django 4.2.7 on 2024-03-13 07:49

from django.db import migrations, models
import django.db.models.deletion
from wooster_django.orders.models import NumberField


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="grand_total",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name="grand total"),
        ),
        migrations.AddField(
            model_name="invoice",
            name="subtotal",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name="subtotal"),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="notes",
            field=models.TextField(blank=True, verbose_name="notes"),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="number",
            field=NumberField(
                document_type="Invoice",
                editable=False,
                padding=4,
                prefix="INV-",
                start_index=1000,
                verbose_name="number",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[("draft", "Draft"), ("stimate", "Estimate"), ("invoiced", "Invoiced"), ("paid", "Paid")],
                default="draft",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="terms",
            field=models.TextField(blank=True, verbose_name="terms"),
        ),
        migrations.CreateModel(
            name="InvoiceLine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rank", models.PositiveSmallIntegerField(verbose_name="rank")),
                ("description", models.CharField(max_length=100, verbose_name="description")),
                ("quantity", models.DecimalField(decimal_places=5, default=1, max_digits=15, verbose_name="quantity")),
                (
                    "unit_price",
                    models.DecimalField(decimal_places=4, default=0, max_digits=15, verbose_name="unit price"),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.invoice", verbose_name="invoice"
                    ),
                ),
            ],
        ),
    ]
