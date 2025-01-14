from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from online.models import OnlineRec
from pages.models import PriceList, PriceList1


User = get_user_model()


class OnlineRecModelTestCase(TestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Создание тестовых прайс-листов
        self.price_list_manicure = PriceList.objects.create(
            service='Маникюр',
            price='300 рублей'
        )
        self.price_list_pedicure = PriceList1.objects.create(
            service='Педикюр',
            price='400 рублей'
        )

    def test_create_online_rec(self):
        """Тест создания онлайн-записи."""
        online_rec = OnlineRec.objects.create(
            user=self.user,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            service_type='manicure'
        )

        # Добавление услуг маникюра
        online_rec.service_manicure.set([self.price_list_manicure])

        # Проверка, что объект был создан с правильными полями
        self.assertEqual(online_rec.user, self.user)
        self.assertEqual(online_rec.service_type, 'manicure')
        self.assertEqual(online_rec.service_manicure.count(), 1)
        self.assertEqual(str(online_rec),
                         f'Запись от {self.user} на Маникюр '
                         f'{online_rec.appointment_date} в '
                         f'{online_rec.appointment_time}')

    def test_unique_appointment_time(self):
        """Тест проверки уникальности времени записи."""
        # Создаем первую запись
        OnlineRec.objects.create(
            user=self.user,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            service_type='manicure'
        )

        # Пытаемся создать вторую запись с тем же временем
        with self.assertRaises(ValidationError):
            online_rec = OnlineRec(
                user=self.user,
                appointment_date=timezone.now().date(),
                appointment_time=timezone.now().time(),
                # Используем объект времени
                service_type='manicure'
            )
            online_rec.clean()
            online_rec.save()

    def test_string_representation(self):
        """Тест строкового представления онлайн-записи."""
        online_rec = OnlineRec.objects.create(
            user=self.user,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            service_type='manicure'
        )
        online_rec.service_manicure.set(
            [self.price_list_manicure])
        expected_str = f'Запись от {self.user} на Маникюр '\
                       f'{online_rec.appointment_date} в '\
                       f'{online_rec.appointment_time}'
        self.assertEqual(str(online_rec), expected_str)
