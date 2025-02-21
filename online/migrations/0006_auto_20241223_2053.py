# Generated by Django 3.2.16 on 2024-12-23 17:53

from django.db import migrations, models
import django.utils.timezone
import online.validators


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0005_alter_onlinerec_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinerec',
            name='appointment_date',
            field=models.DateField(default=django.utils.timezone.now, validators=[online.validators.validate_appointment_date], verbose_name='Дата проведения услуги'),
        ),
        migrations.AlterField(
            model_name='onlinerec',
            name='service_status',
            field=models.CharField(choices=[('created', 'Создана'), ('confirmed', 'Подтверждена'), ('postponed', 'Перенесена'), ('cancelled', 'Отменена'), ('completed', 'Выполнена')], default='created', max_length=20, verbose_name='Статус услуги'),
        ),
        migrations.AlterField(
            model_name='onlinerec',
            name='service_type',
            field=models.CharField(choices=[('manicure', 'Маникюр'), ('pedicure', 'Педикюр'), ('manicure&pedicure', 'Маникюр и педикюр')], max_length=20, verbose_name='Тип услуги'),
        ),
    ]
