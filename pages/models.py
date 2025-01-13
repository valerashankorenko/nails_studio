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


class PriceListBase(models.Model):
    """
    Абстрактная модель для прайс-листа.
    """
    service = models.CharField(
        'Название услуги',
        max_length=150,
        unique=True,
    )
    price = models.CharField(
        'Стоимость услуги',
        max_length=20
    )

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return f'{self.service} - {self.price}'


class PriceList(PriceListBase):
    """
    Модель для прайс-листа маникюра.
    """
    class Meta(PriceListBase.Meta):
        verbose_name = 'прайс-лист маникюр'
        verbose_name_plural = 'Прайс-лист маникюр'


class PriceList1(PriceListBase):
    """
    Модель для прайс-листа педикюра.
    """
    class Meta(PriceListBase.Meta):
        verbose_name = 'прайс-лист педикюр'
        verbose_name_plural = 'Прайс-лист педикюр'


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
