from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'text', 'created_at_format', 'is_published')
    list_display_links = ('created_at_format', 'author',)
    search_fields = ('created_at_format', 'author',)
    empty_value_display = '-пусто-'

    def created_at_format(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M:%S')

    created_at_format.short_description = 'Дата и время отзыва'
