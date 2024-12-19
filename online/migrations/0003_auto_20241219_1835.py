# Generated by Django 3.2.16 on 2024-12-19 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20241218_2145'),
        ('online', '0002_alter_onlinerec_service_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinerec',
            name='service',
        ),
        migrations.AddField(
            model_name='onlinerec',
            name='service_manicure',
            field=models.ManyToManyField(blank=True, related_name='online_recs', to='pages.PriceList', verbose_name='Услуги маникюра'),
        ),
        migrations.AddField(
            model_name='onlinerec',
            name='service_pedicure',
            field=models.ManyToManyField(blank=True, related_name='online_recs_pedicure', to='pages.PriceList1', verbose_name='Услуги педикюра'),
        ),
        migrations.AddField(
            model_name='onlinerec',
            name='service_status',
            field=models.CharField(choices=[('created', 'Создана'), ('confirmed', 'Подтверждена'), ('postponed', 'Перенесена'), ('cancelled', 'Отменена')], default='created', max_length=20, verbose_name='Статус услуги'),
        ),
        migrations.AlterField(
            model_name='onlinerec',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='onlinerec',
            name='service_type',
            field=models.CharField(choices=[('manicure', 'Маникюр'), ('pedicure', 'Педикюр')], default='manicure', max_length=20, verbose_name='Тип услуги'),
        ),
    ]
