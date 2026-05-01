from django.contrib import admin
from .models import Product, RecipeItem

class RecipeItemInline(admin.TabularInline):
    model  = RecipeItem
    extra  = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines      = [RecipeItemInline]