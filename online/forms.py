from django import forms
from django.core.exceptions import ValidationError
from online.models import OnlineRec
from datetime import time


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
        fields = [
            'user',
            'appointment_date',
            'appointment_time',
            'service_type',
            'service_manicure',
            'service_pedicure',
        ]
        widgets = {
            'service_manicure': forms.CheckboxSelectMultiple(),
            'service_pedicure': forms.CheckboxSelectMultiple(),
            'user': forms.Select(),
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].choices = get_available_time_slots()

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        return time(int(appointment_time.split(':')[0]), 0)

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if not appointment_date:
            self.add_error(
                'appointment_date',
                'Это поле обязательно для заполнения.'
            )
        if not appointment_time:
            self.add_error(
                'appointment_time',
                'Это поле обязательно для заполнения.'
            )

        if appointment_date and appointment_time:
            # Проверка на наличие записи с той же датой и временем
            existing_records = OnlineRec.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            if self.instance.pk:
                existing_records = existing_records.exclude(
                    pk=self.instance.pk
                )

            if existing_records.exists():
                raise ValidationError(
                    'На выбранную дату и время уже есть запись. '
                    'Пожалуйста, выберите другое время.'
                )

        return cleaned_data
