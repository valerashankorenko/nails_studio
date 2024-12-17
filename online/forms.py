from django import forms
from .models import OnlineRec


class OnlineRecForm(forms.ModelForm):
    class Meta:
        model = OnlineRec
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        manicure_services = cleaned_data.get('manicure_services')
        pedicure_services = cleaned_data.get('pedicure_services')

        if service_type == 'manicure':
            if manicure_services and manicure_services.count() > 3:
                raise forms.ValidationError(
                    'Можно выбрать максимум 3 услуги маникюра'
                )
            # Очищаем поле педикюра при выборе маникюра
            cleaned_data['pedicure_services'] = None

        if service_type == 'pedicure':
            if pedicure_services and pedicure_services.count() > 3:
                raise forms.ValidationError(
                    'Можно выбрать максимум 3 услуги педикюра'
                )
            # Очищаем поле маникюра при выборе педикюра
            cleaned_data['manicure_services'] = None

        return cleaned_data
