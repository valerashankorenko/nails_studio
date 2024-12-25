from django.contrib import admin
from .forms import OnlineRecAdminForm
from .models import OnlineRec


@admin.register(OnlineRec)
class OnlineRecAdmin(admin.ModelAdmin):
    form = OnlineRecAdminForm
    list_display = (
        'get_user_name',
        'phone_number',
        'appointment_datetime_format',
        'service_status',
        'service_manicure_count',
        'service_pedicure_count'
    )
    list_display_links = (
        'get_user_name',
        'appointment_datetime_format'
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__phone_number'
    )
    filter_horizontal = (
        'service_manicure',
        'service_pedicure'
    )
    empty_value_display = '-пусто-'

    @admin.display(description='Клиент')
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    @admin.display(description='Номер телефона')
    def phone_number(self, obj):
        return getattr(obj.user, 'phone_number', 'Нет номера')

    @admin.display(description='Дата и время проведения услуги')
    def appointment_datetime_format(self, obj):
        return f'{obj.appointment_date:%d.%m.%Y} {obj.appointment_time:%H:%M}'

    @admin.display(description='Кол-во услуг маникюра')
    def service_manicure_count(self, obj):
        return obj.service_manicure.count()

    @admin.display(description='Кол-во услуг педикюра')
    def service_pedicure_count(self, obj):
        return obj.service_pedicure.count()
