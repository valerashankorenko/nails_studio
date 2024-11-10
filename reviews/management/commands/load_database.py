import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Review
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузить данные в модель отзывов'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'Загрузка пользователей и отзывов в базу начата'))
        with open('data/users.json', encoding='utf-8') as data_file_users:
            user_data = json.loads(data_file_users.read())
            for user in user_data:
                user_password = make_password(
                    user['password'])  # Хэшируем пароль
                try:
                    User.objects.get_or_create(
                        username=user['username'],
                        defaults={
                            'email': user['email'],
                            'password': user_password,
                            'phone_number': user.get('phone_number')
                        }
                    )
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(
                        f"Пользователь {user['username']} уже существует."))

        with open('data/review.json', encoding='utf-8',
                  ) as data_file_review:
            review_data = json.loads(data_file_review.read())
            for review in review_data:
                Review.objects.get_or_create(**review)

        self.stdout.write(self.style.SUCCESS('Данные загружены'))
