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
                raise forms.ValidationError(
                    'Выбранное время уже занято. '
                    'Пожалуйста, выберите другое время.'
                )

        return cleaned_data


class OnlineRecAdminForm(OnlineRecForm):
    """
    Форма для админки с добавлением поля пользователя.
    """
    class Meta(OnlineRecForm.Meta):
        fields = OnlineRecForm.Meta.fields + ('user',)
