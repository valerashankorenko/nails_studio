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
        auto_now_add=True,
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

    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    """
    Модель для лайков отзывов клиентов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f'{self.user} liked {self.review}'
