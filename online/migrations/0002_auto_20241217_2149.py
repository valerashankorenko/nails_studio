# Generated by Django 3.2.16 on 2024-12-17 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0006_auto_20241217_2149'),
        ('online', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinerec',
            name='service',
        ),
        migrations.RemoveField(
            model_name='onlinerec',
            name='service1',
        ),
        migrations.AddField(
            model_name='onlinerec',
            name='manicure_service',
            field=models.ForeignKey(blank=True, limit_choices_to={'service_type': 'manicure'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.pricelist', verbose_name='Услуга маникюра'),
        ),
        migrations.AddField(
            model_name='onlinerec',
            name='pedicure_service',
            field=models.ForeignKey(blank=True, limit_choices_to={'service_type': 'pedicure'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.pricelist1', verbose_name='Услуга педикюра'),
        ),
        migrations.AlterField(
            model_name='onlinerec',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
    ]