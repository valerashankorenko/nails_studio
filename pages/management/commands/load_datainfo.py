import json
import logging

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from pages.models import Info, PriceList, PriceList1

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загрузить тестовых данных в модель прайс-лист и советы'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Загрузка в базу начата'))

        self.load_info()
        self.load_price_list()
        self.load_price_list1()

        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def load_info(self):
        try:
            with open('data/info.json', encoding='utf-8') as data_file_info:
                info_data = json.load(data_file_info)
                for info in info_data:
                    try:
                        Info.objects.get_or_create(**info)
                    except ValidationError as e:
                        self.stdout.write(
                            self.style.ERROR(f'Ошибка в данных Info: {e}'))
                        logger.error(f'Ошибка в данных Info: {e}')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл info.json не найден.'))
            logger.error('Файл info.json не найден.')
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла info.json.'))
            logger.error(
                'Ошибка при чтении JSON. Проверьте формат файла info.json.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке данных Info: {str(e)}'))
            logger.error(f'Произошла ошибка при загрузке данных Info: {str(e)}')

    def load_price_list(self):
        try:
            with open('data/price.json', encoding='utf-8') as data_file_price:
                price_data = json.load(data_file_price)
                for price in price_data:
                    try:
                        PriceList.objects.get_or_create(**price)
                    except ValidationError as e:
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка в данных PriceList: {e}'))
                        logger.error(f'Ошибка в данных PriceList: {e}')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл price.json не найден.'))
            logger.error('Файл price.json не найден.')
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла price.json.'))
            logger.error(
                'Ошибка при чтении JSON. Проверьте формат файла price.json.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке данных PriceList: {str(e)}'))
            logger.error(
                f'Произошла ошибка при загрузке данных PriceList: {str(e)}')

    def load_price_list1(self):
        try:
            with open('data/price1.json', encoding='utf-8') as data_file_price1:
                price_data = json.load(data_file_price1)
                for price in price_data:
                    try:
                        PriceList1.objects.get_or_create(**price)
                    except ValidationError as e:
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка в данных PriceList1: {e}'))
                        logger.error(f'Ошибка в данных PriceList1: {e}')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл price1.json не найден.'))
            logger.error('Файл price1.json не найден.')
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(
                'Ошибка при чтении JSON. Проверьте формат файла price1.json.'))
            logger.error(
                'Ошибка при чтении JSON. Проверьте формат файла price1.json.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке данных PriceList1: {str(e)}'))
            logger.error(
                f'Произошла ошибка при загрузке данных PriceList1: {str(e)}')
