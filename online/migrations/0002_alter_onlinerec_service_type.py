# Generated by Django 3.2.16 on 2024-12-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinerec',
            name='service_type',
            field=models.CharField(choices=[('manicure', 'Маникюр'), ('pedicure', 'Педикюр')], max_length=20, verbose_name='Тип услуги'),
        ),
    ]