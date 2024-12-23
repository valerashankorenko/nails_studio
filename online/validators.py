from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_appointment_date(value):
    """
    Валидатор даты для оказания услуги
    """
    now = timezone.now().date()

    if value < now:
        raise ValidationError('Дата не может быть в прошлом.')

