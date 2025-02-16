from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class BaseProfileForm(forms.ModelForm):
    """
    Базовая форма для профиля пользователя.
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
        )


class ProfileCreateForm(UserCreationForm):
    """
    Форма для создания пользователя.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = BaseProfileForm.Meta.fields


class ProfileUpdateForm(BaseProfileForm):
    """
    Форма для редактирования профиля пользователя.
    """
    pass
