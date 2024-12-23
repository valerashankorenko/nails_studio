from django import forms
from django.core.exceptions import ValidationError

from online.models import OnlineRec


def get_available_time_slots():
    start_hour = 8
    end_hour = 20
    time_slots = []
    for hour in range(start_hour, end_hour):
        time_slots.append((f'{hour:02}:00', f'{hour:02}:00'))
        time_slots.append((f'{hour:02}:30', f'{hour:02}:30'))
    time_slots.append((f'{end_hour:02}:00', f'{end_hour:02}:00'))
    return time_slots


class OnlineRecForm(forms.ModelForm):
    """
    Форма для создания/редактирования онлайн-записи.
    """

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
            'appointment_time': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].choices = get_available_time_slots()

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            # Проверка на наличие записи с той же датой и временем
            existing_records = OnlineRec.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            if self.instance.pk:
                existing_records = existing_records.exclude(
                    pk=self.instance.pk)

            if existing_records.exists():
                raise ValidationError(
                    f'На выбранную дату и время уже есть запись. '
                    f'Пожалуйста, выберите другое время.'
                )
        return cleaned_data
