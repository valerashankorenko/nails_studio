from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    """
    Форма для создания и редактирования отзывов клиентов
    """
    class Meta:
        model = Review
        fields = ('text',)
