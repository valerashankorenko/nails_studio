import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание суперпользователя из переменных среды.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME')
        last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME')
        phone_number = os.environ.get('DJANGO_SUPERUSER_PHONE_NUMBER')

        missing_vars = [var for var in [
            username, email, password] if var is None]
        if missing_vars:
            self.stdout.write(self.style.ERROR(
                'Ошибка: Необходимые переменные среды не установлены: {}'
                .format(', '.join(missing_vars))
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                'Суперпользователь с данным email ({}) уже существует.'
                .format(email)))
            return
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                'Суперпользователь с данным именем пользователя '
                '({}) уже существует.'.format(username)))
            return

        if phone_number and User.objects.filter(
                phone_number=phone_number).exists():
            self.stdout.write(self.style.WARNING(
                'Суперпользователь с данным номером телефона ({}) '
                'уже существует.'.format(phone_number)))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        self.stdout.write(self.style.SUCCESS(
            'Успешно создан новый суперпользователь: {}'.format(username)))
