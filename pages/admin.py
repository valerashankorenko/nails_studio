from django.contrib import admin

from .models import Foto, PriceList, PriceList1, Info


@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'pub_date_format')
    list_display_links = ('image', 'pub_date_format')
    search_fields = ('image', 'pub_date')
    empty_value_display = '-пусто-'

    def pub_date_format(self, obj):
        return obj.pub_date.strftime('%d-%m-%Y %H:%M:%S')

    pub_date_format.short_description = 'Дата загрузки фотографии'


@admin.register(PriceList, PriceList1)
class PriceListAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'service', 'price')
    list_display_links = ('service', 'price')
    search_fields = ('service', 'price')
    ordering = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'text')
    list_display_links = ('title', 'text')
    search_fields = ('title', 'text')

