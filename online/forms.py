from datetime import datetime

from django import forms
from online.models import OnlineRec


class OnlineRecForm(forms.ModelForm):
    appointment_time = forms.ChoiceField(
        label='Время проведения услуги',
        choices=[],
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
        appointment_date = self.data.get('appointment_date')
        if appointment_date:
            appointment_date = datetime.strptime(
                appointment_date, '%Y-%m-%d').date()
            self.fields['appointment_time'].choices = (
                self.get_available_time_slots(appointment_date)
            )

    def get_available_time_slots(self, appointment_date=None):
        if appointment_date is None:
            return []

        # Получаем занятые временные слоты для выбранной даты
        occupied_slots = OnlineRec.objects.filter(
            appointment_date=appointment_date
        ).values_list('appointment_time', flat=True)

        # Приводим занятые слоты к формату HH:MM
        occupied_slots = [slot.strftime('%H:%M') for slot in occupied_slots]

        # Генерируем все возможные слоты
        start_hour = 8
        end_hour = 19
        time_slots = []

        for hour in range(start_hour, end_hour + 1):
            time_slot = f'{hour:02}:00'
            if time_slot not in occupied_slots:
                time_slots.append((time_slot, time_slot))

        return time_slots

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            # Проверяем, занят ли выбранный временной слот
            if OnlineRec.objects.filter(
                    appointment_date=appointment_date,
                    appointment_time=appointment_time
            ).exists():
                formatted_date = appointment_date.strftime('%d.%m.%Y')
                raise forms.ValidationError(
                    {
                        'appointment_time': f'На {formatted_date} в '
                                            f'{appointment_time} уже есть '
                                            f'запись. Пожалуйста, выберите '
                                            f'другое время.'}
                )

        return cleaned_data


class OnlineRecAdminForm(OnlineRecForm):
    """
    Форма для админки с добавлением поля пользователя.
    """
    class Meta(OnlineRecForm.Meta):
        fields = OnlineRecForm.Meta.fields + ('user',)
