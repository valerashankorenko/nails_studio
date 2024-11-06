from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """
    Модель для отзывов клиентов.
    """
    text = models.TextField(
        'Текст отзыва',
        max_length=500,
    )
    created_at = models.DateTimeField(
        'Дата и время публикации отзыва',
        auto_now=True,
    )
    author = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    is_published = models.BooleanField(
        'Опубликовано', default=False,
        help_text='Поставьте галочку, чтобы опубликовать отзыв.')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.author} {self.created_at}'
