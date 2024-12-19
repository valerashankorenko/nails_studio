# Generated by Django 3.2.16 on 2024-12-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20241130_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'verbose_name': 'прайс-лист маникюр', 'verbose_name_plural': 'Прайс-лист маникюр'},
        ),
        migrations.AlterModelOptions(
            name='pricelist1',
            options={'verbose_name': 'прайс-лист педикюр', 'verbose_name_plural': 'Прайс-лист педикюр'},
        ),
        migrations.AddField(
            model_name='pricelist',
            name='service_type',
            field=models.CharField(default=1, max_length=20, verbose_name='Тип услуги'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricelist1',
            name='service_type',
            field=models.CharField(default=123, max_length=20, verbose_name='Тип услуги'),
            preserve_default=False,
        ),
    ]