from datetime import time, datetime
from django.core.exceptions import ValidationError


def validate_appointment_time(value):
    """
    Валидатор времени для оказания услуги
    """
    now = datetime.now().time()
    if not (time(9, 0) <= value <= time(20, 0)):
        raise ValidationError('Время должно быть в диапазоне с 9:00 до 20:00.')

    if value.minute != 0:
        raise ValidationError(
            'Время должно быть на целый час (например, 9:00, 10:00 и т.д.).')

    if value < now:
        raise ValidationError('Время не может быть в прошлом.')
