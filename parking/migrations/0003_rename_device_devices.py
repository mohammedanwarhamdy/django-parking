# Generated by Django 4.2.10 on 2024-02-25 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_remove_device_stause'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='device',
            new_name='devices',
        ),
    ]
