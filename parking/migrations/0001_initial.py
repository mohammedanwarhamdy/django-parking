# Generated by Django 4.2.10 on 2024-02-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address')),
                ('Mack', models.CharField(blank=True, max_length=30, null=True, verbose_name='Mack Address')),
                ('Device_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Device Name')),
                ('stause', models.BooleanField(default='True', verbose_name='Statuse')),
            ],
        ),
    ]
