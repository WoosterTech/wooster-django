# Generated by Django 4.2.7 on 2023-12-06 07:32

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0007_alter_item_parent_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="common_color",
            field=colorfield.fields.ColorField(
                blank=True,
                choices=[
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
                ],
                default="",
                image_field=None,
                max_length=25,
                samples=None,
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="item_categories",
            field=models.ManyToManyField(to="inventory.itemcategory", verbose_name="item categories"),
        ),
        migrations.AddField(
            model_name="item",
            name="size",
            field=models.CharField(
                blank=True, help_text="e.g. small/medium/large or '32 oz.'", max_length=50, verbose_name="size"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="true_color",
            field=colorfield.fields.ColorField(
                blank=True,
                default="",
                image_field=None,
                max_length=25,
                samples=[
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
                ],
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(max_length=100, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="contact_email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="contact email"),
        ),
    ]