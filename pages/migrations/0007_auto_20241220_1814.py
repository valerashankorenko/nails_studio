# Generated by Django 3.2.16 on 2024-12-20 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20241219_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'ordering': ('id',), 'verbose_name': 'прайс-лист маникюр', 'verbose_name_plural': 'Прайс-лист маникюр'},
        ),
        migrations.AlterModelOptions(
            name='pricelist1',
            options={'ordering': ('id',), 'verbose_name': 'прайс-лист педикюр', 'verbose_name_plural': 'Прайс-лист педикюр'},
        ),
    ]
