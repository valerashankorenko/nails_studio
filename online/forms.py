from django import forms
from .models import OnlineRec


class OnlineRecForm(forms.ModelForm):
    class Meta:
        model = OnlineRec
        fields = '__all__'
        widgets = {
            'service_manicure': forms.CheckboxSelectMultiple(),
            'service_pedicure': forms.CheckboxSelectMultiple(),
            'user': forms.Select()
        }
