# Generated by Django 4.2.7 on 2024-02-12 09:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0007_documentnumbers"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DocumentNumbers",
            new_name="DocumentNumber",
        ),
    ]
