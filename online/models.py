from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

from online.validators import validate_appointment_time
from pages.models import PriceList, PriceList1

User = get_user_model()


class OnlineRec(models.Model):
    """
    Модель для онлайн-записи
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    created_at = models.DateTimeField(
        'Дата создания записи',
        auto_now_add=True
    )
    appointment_date = models.DateField(
        'Дата проведения услуги',
        default=date.today
    )
    appointment_time = models.TimeField(
        'Время проведения услуги',
        default=None,
        blank=True,
        null=True,
        validators=[validate_appointment_time],
    )
    service_status = models.CharField(
        'Статус услуги',
        max_length=20,
        choices=[
            ('created', 'Создана'),
            ('confirmed', 'Подтверждена'),
            ('postponed', 'Перенесена'),
            ('cancelled', 'Отменена'),
            ('completed', 'Выполнена'),
        ],
        default='created'
    )
    service_type = models.CharField(
        'Тип услуги',
        max_length=20,
        choices=[
            ('manicure', 'Маникюр'),
            ('pedicure', 'Педикюр'),
            ('manicure&pedicure', 'Маникюр и педикюр'),
        ],
    )
    service_manicure = models.ManyToManyField(
        PriceList,
        blank=True,
        verbose_name='Услуги маникюра',
        related_name='online_recs'
    )
    service_pedicure = models.ManyToManyField(
        PriceList1,
        blank=True,
        verbose_name='Услуги педикюра',
        related_name='online_recs_pedicure'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'онлайн-запись'
        verbose_name_plural = 'Онлайн-записи'

    def __str__(self):
        return (f'Запись от {self.user} на {self.get_service_type_display()}'
                f' {self.appointment_date} в {self.appointment_time}')
