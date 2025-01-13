import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Review

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загрузить данные в модель отзывов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Загрузка пользователей и отзывов в базу начата'))

        self.load_users()
        self.load_reviews()

        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def load_users(self):
        try:
            with open('data/users.json', encoding='utf-8') as data_file_users:
                user_data = json.load(data_file_users)
                for user in user_data:
                    user_password = make_password(user['password']) # Хэшируем пароль
                    try:
                        User.objects.get_or_create(
                            username=user['username'],
                            defaults={
                                'email': user['email'],
                                'password': user_password,
                                'phone_number': user.get('phone_number'),
                                'first_name': user.get('first_name'),
                                'last_name': user.get('last_name')
                            }
                        )
                    except IntegrityError:
                        self.stdout.write(self.style.ERROR(
                            f"Пользователь {user['username']} уже существует."
                        ))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл users.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке пользователей: {str(e)}'))

    def load_reviews(self):
        try:
            with open('data/review.json', encoding='utf-8') as data_file_review:
                review_data = json.load(data_file_review)
                for review in review_data:
                    try:
                        Review.objects.get_or_create(**review)
                    except IntegrityError:
                        self.stdout.write(self.style.ERROR(
                            f"Отзыв с идентификатором "
                            f"{review.get('id')} уже существует."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'Файл review.json не найден.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке отзывов: {str(e)}'))
