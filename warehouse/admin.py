from django.contrib import admin
from .models import Ingredient, Batch
from django.utils import timezone

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display  = ['name', 'unit']
    search_fields = ['name']

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display  = ['lot_number', 'ingredient', 'quantity',
                     'received_at', 'expiry_date', 'days_left_display', 'status_display']
    list_filter   = ['status', 'ingredient']
    search_fields = ['lot_number', 'ingredient__name']
    ordering      = ['expiry_date']

    def days_left_display(self, obj):
        d = obj.days_left
        if d < 0:   return f'Просрочено на {abs(d)} дн.'
        if d <= 30: return f'⚠ {d} дн.'
        return f'{d} дн.'
    days_left_display.short_description = 'Дней до истечения'

    def status_display(self, obj):
        labels = {'ok': '✅ OK', 'warning': '⚠ Скоро', 'expired': '❌ Просрочено'}
        return labels.get(obj.status_label, obj.status)
    status_display.short_description = 'Статус'