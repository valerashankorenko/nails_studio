import json

from django.core.management.base import BaseCommand

from pages.models import Info, PriceList, PriceList1


class Command(BaseCommand):
    help = 'Загрузить тестовых данных в модель прайс-лист и советы'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'Загрузка в базу начата'))

        with open('data/info.json', encoding='utf-8',
                  ) as data_file_info:
            info_data = json.loads(data_file_info.read())
            for info in info_data:
                Info.objects.get_or_create(**info)

        with open('data/price.json', encoding='utf-8',
                  ) as data_file_price:
            price_data = json.loads(data_file_price.read())
            for price in price_data:
                PriceList.objects.get_or_create(**price)

        with open('data/price1.json', encoding='utf-8',
                  ) as data_file_price:
            price_data = json.loads(data_file_price.read())
            for price in price_data:
                PriceList1.objects.get_or_create(**price)

        self.stdout.write(self.style.SUCCESS('Данные загружены'))
