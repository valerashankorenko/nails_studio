from django.db import models


class Foto(models.Model):
    """
    Модель для фотографий работ.
    """
    image = models.ImageField(
        'Фотографии работ',
        upload_to='app/')
    pub_date = models.DateTimeField(
        'Дата загрузки фотографии',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'фотография работы'
        verbose_name_plural = 'Фотографии работ'

    def __str__(self):
        return f'Фотография работы №{self.id}'


class PriceList(models.Model):
    """
    Модель для прайс-листа.
    """
    service = models.CharField(
        'Название услуги',
        max_length=150, )
    price = models.CharField(
        'Стоимость услуги',
        max_length=20, )

    class Meta:
        verbose_name = 'прайс-лист'
        verbose_name_plural = 'Прайс-лист'

    def __str__(self):
        return f'{self.service} - {self.price}'


class Info(models.Model):
    """
    Модель для советов.
    """
    title = models.CharField(
        'Заголовок совета', max_length=256)
    text = models.TextField('Текст совета')

    class Meta:
        verbose_name = 'совет'
        verbose_name_plural = 'Советы'

    def __str__(self):
        return f'{self.text}'
