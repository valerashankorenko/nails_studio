from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from online.validators import validate_appointment_date
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
        default=timezone.now,
        validators=[validate_appointment_date],
    )
    appointment_time = models.TimeField(
        'Время проведения услуги',
        default=None,
        blank=True,
        null=True
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
        return (f'Запись от {self.user} на {self.get_service_type_display()} '
                f'{self.appointment_date} в {self.appointment_time}')

    def clean(self):
        super().clean()

        # Проверка на дублирование записи на тот же день и время
        if self.appointment_date and self.appointment_time:
            existing_records = OnlineRec.objects.filter(
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time
            )
            if self.pk:
                existing_records = existing_records.exclude(pk=self.pk)

            if existing_records.exists():
                formatted_date = self.appointment_date.strftime('%d.%m.%Y')
                formatted_time = self.appointment_time.strftime('%H:%M')
                raise ValidationError(
                    f'На {formatted_date} в {formatted_time} уже есть запись. '
                    f'Пожалуйста, выберите другое время.'
                )
