# Generated by Django 3.2.16 on 2024-12-19 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20241218_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricelist',
            name='service_type',
        ),
        migrations.RemoveField(
            model_name='pricelist1',
            name='service_type',
        ),
    ]
