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
    Модель для прайс-листа маникюра.
    """
    service = models.CharField(
        'Название услуги',
        max_length=150, )
    price = models.CharField(
        'Стоимость услуги',
        max_length=20)
    service_type = models.CharField(
        'Тип услуги',
        max_length=20,
        default='manicure'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'прайс-лист маникюр'
        verbose_name_plural = 'Прайс-лист маникюр'

    def __str__(self):
        return f'{self.service} - {self.price}'


class PriceList1(models.Model):
    """
    Модель для прайс-листа педикюра.
    """
    service = models.CharField(
        'Название услуги',
        max_length=150, )
    price = models.CharField(
        'Стоимость услуги',
        max_length=20)
    service_type = models.CharField(
        'Тип услуги',
        max_length=20,
        default='pedicure'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'прайс-лист педикюр'
        verbose_name_plural = 'Прайс-лист педикюр'

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
