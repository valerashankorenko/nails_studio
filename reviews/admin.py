from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_author_name', 'text', 'created_at_format', 'is_published'
    )
    list_display_links = ('created_at_format', 'get_author_name',)
    search_fields = ('text', 'author__email',)
    ordering = ('id', 'is_published',)
    empty_value_display = '-пусто-'

    def get_author_name(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'
    get_author_name.short_description = 'Автор отзыва'

    def created_at_format(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')

    created_at_format.short_description = 'Дата и время отзыва'

