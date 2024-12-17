from django.contrib import admin
from django.forms import HiddenInput  # добавляем импорт
from .models import OnlineRec
from .forms import OnlineRecForm


@admin.register(OnlineRec)
class OnlineRecAdmin(admin.ModelAdmin):
    form = OnlineRecForm
    list_display = (
        'get_user_name', 'appointment_datetime_format', 'created_at_format'
    )
    list_display_links = ('get_user_name', 'appointment_datetime_format',)
    search_fields = ('user__username',)
    empty_value_display = '-пусто-'

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields': (
                    'user',
                    'appointment_date',
                    'appointment_time',
                    'service_type',
                    'manicure_services',
                    'pedicure_services'
                )
            }),
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # если это редактирование существующей записи
            if obj.service_type == 'manicure':
                form.base_fields['pedicure_services'].widget = HiddenInput()
            else:
                form.base_fields['manicure_services'].widget = HiddenInput()
        return form

    @admin.display(description='Клиент')
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    @admin.display(description='Дата и время проведения услуги')
    def appointment_datetime_format(self, obj):
        return f"{obj.appointment_date.strftime('%d-%m-%Y')} {obj.appointment_time.strftime('%H:%M')}"

    @admin.display(description='Дата создания записи')
    def created_at_format(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')