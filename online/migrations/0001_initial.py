# Generated by Django 3.2.16 on 2024-12-17 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0005_auto_20241217_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineRec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания записи')),
                ('appointment_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата проведения услуги')),
                ('appointment_time', models.TimeField(default=django.utils.timezone.now, verbose_name='Время проведения услуги')),
                ('service_type', models.CharField(choices=[('manicure', 'Маникюр'), ('pedicure', 'Педикюр')], default='manicure', max_length=20, verbose_name='Тип услуги')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.pricelist', verbose_name='Услуга маникюра')),
                ('service1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.pricelist1', verbose_name='Услуга педикюра')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'онлайн-запись',
                'verbose_name_plural': 'Онлайн-записи',
                'ordering': ('-created_at',),
            },
        ),
    ]