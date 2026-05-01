from django.db import models
from warehouse.models import Ingredient

class Product(models.Model):
    name        = models.CharField(max_length=200, verbose_name='Название продукта')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class RecipeItem(models.Model):
    product           = models.ForeignKey(Product, on_delete=models.CASCADE,
                                          related_name='recipe_items', verbose_name='Продукт')
    ingredient        = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                          verbose_name='Сырьё')
    quantity_per_unit = models.DecimalField(max_digits=10, decimal_places=5,
                                            verbose_name='Норма на 1 шт')

    def total_for(self, quantity):
        return self.quantity_per_unit * quantity

    class Meta:
        verbose_name = 'Состав рецептуры'

    def __str__(self):
        return f'{self.ingredient.name} - {self.product.name}'
    