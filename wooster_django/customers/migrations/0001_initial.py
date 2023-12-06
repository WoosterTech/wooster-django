# Generated by Django 4.2.7 on 2023-12-04 09:56

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("organization_name", models.CharField(max_length=100, unique=True, verbose_name="organization name")),
                ("contact_name", models.CharField(max_length=100, verbose_name="contact full name")),
                ("contact_email", models.EmailField(blank=True, max_length=254, verbose_name="contact email")),
                (
                    "contact_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None, verbose_name="contact phone number"
                    ),
                ),
            ],
        ),
    ]