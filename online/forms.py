from django import forms
from online.models import OnlineRec


def get_available_time_slots():
    """
    Функция для создания доступных временных слотов.
    """
    start_hour = 8
    end_hour = 19
    time_slots = []
    for hour in range(start_hour, end_hour + 1):
        time_slots.append((f'{hour:02}:00', f'{hour:02}:00'))
    return time_slots


class OnlineRecForm(forms.ModelForm):
    """
    Форма для создания/редактирования онлайн-записи.
    """
    appointment_time = forms.ChoiceField(
        label='Время проведения услуги',
        choices=get_available_time_slots(),
        required=True
    )

    class Meta:
        model = OnlineRec
        fields = (
            'appointment_date',
            'appointment_time',
            'service_type',
            'service_manicure',
            'service_pedicure',
        )
        widgets = {
            'service_manicure': forms.CheckboxSelectMultiple(),
            'service_pedicure': forms.CheckboxSelectMultiple(),
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].choices = get_available_time_slots()


class OnlineRecAdminForm(OnlineRecForm):
    """
    Форма для админки с добавлением поля пользователя.
    """
    class Meta(OnlineRecForm.Meta):
        fields = OnlineRecForm.Meta.fields + ('user',)
