# Generated by Django 4.2 on 2023-04-10 23:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("remesh_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="sent_date",
            new_name="sent_datetime",
        ),
        migrations.RenameField(
            model_name="thought",
            old_name="sent_date",
            new_name="sent_datetime",
        ),
    ]
