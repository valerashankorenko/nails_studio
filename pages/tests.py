from django.test import TestCase
from pages.models import PriceList


class PriceListModelTestCase(TestCase):
    def test_create_price_list(self):
        """Тест создания прайс-листа."""
        price_list = PriceList.objects.create(
            service='Название услуги',
            price='250 рублей',
        )

        # Проверка, что объект был создан с правильными полями
        self.assertEqual(price_list.service, 'Название услуги')
        self.assertEqual(price_list.price, '250 рублей')

        # Проверка, что объект сохранен в базе данных
        self.assertTrue(PriceList.objects.filter(id=price_list.id).exists())

        # Проверка строкового представления
        self.assertEqual(str(price_list), 'Название услуги - 250 рублей')
