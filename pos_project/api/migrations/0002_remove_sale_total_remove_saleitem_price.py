# Generated by Django 5.1.6 on 2025-02-21 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='total',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='price',
        ),
    ]
