from django.contrib import admin
from .models import ProductionOrder

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display  = ['number', 'product', 'quantity', 'status', 'due_date', 'created_at']
    list_filter   = ['status']
    search_fields = ['number', 'product__name']
    readonly_fields = ['number', 'created_at', 'created_by']