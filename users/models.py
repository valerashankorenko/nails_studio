from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя.
    """
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    phone_number = models.CharField(
        'Телефонный номер',
        max_length=13,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^\+375\d{9}$',
                message='Неверный формат номера телефона. Формат номера: '
                        '+375XXXXXXXXX',
            ),
        ],
        help_text='Формат номера: +375XXXXXXXXX',
    )
    is_active = models.BooleanField(
        'Статус пользователя',
        default=True,
        help_text='Снимите галочку, чтобы заблокировать пользователя.',
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        validators=(MinLengthValidator(8), MaxLengthValidator(150)),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
