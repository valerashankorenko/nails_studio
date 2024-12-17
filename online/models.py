from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from pages.models import PriceList, PriceList1

User = get_user_model()


class OnlineRec(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    created_at = models.DateTimeField(
        'Дата создания записи',
        auto_now=True,
    )
    appointment_date = models.DateField(
        'Дата проведения услуги',
        default=timezone.now
    )
    appointment_time = models.TimeField(
        'Время проведения услуги',
        default=timezone.now
    )
    service_type = models.CharField(
        'Тип услуги',
        max_length=20,
        choices=[
            ('manicure', 'Маникюр'),
            ('pedicure', 'Педикюр')
        ],
        default='manicure'
    )
    manicure_services = models.ManyToManyField(
        PriceList,
        verbose_name='Услуги маникюра',
        limit_choices_to={'service_type': 'manicure'},
        blank=True,
        related_name='online_records'
    )
    pedicure_services = models.ManyToManyField(
        PriceList1,
        verbose_name='Услуги педикюра',
        limit_choices_to={'service_type': 'pedicure'},
        blank=True,
        related_name='online_records'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'онлайн-запись'
        verbose_name_plural = 'Онлайн-записи'

    def __str__(self):
        return (f'Запись от {self.user} на {self.get_service_type_display()}'
                f' {self.appointment_date} в {self.appointment_time}')