from django.db import models
from django.utils import timezone
from products.models import Product

class ProductionOrder(models.Model):
    STATUS_CHOICES = [
        ('draft',       'Черновик'),
        ('pending',     'Ожидание сырья'),
        ('in_progress', 'В работе'),
        ('done',        'Завершён'),
        ('cancelled',   'Отменён'),
    ]

    number     = models.CharField(max_length=20, unique=True, verbose_name='Номер', blank=True)
    product    = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    quantity   = models.PositiveIntegerField(verbose_name='Количество, шт')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                  default='draft', verbose_name='Статус')
    due_date   = models.DateField(verbose_name='Срок выпуска')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='Создал')
    notes      = models.TextField(blank=True, verbose_name='Примечания')

    class Meta:
        verbose_name = 'Производственный заказ'
        verbose_name_plural = 'Производственные заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.number} — {self.product}'

    def save(self, *args, **kwargs):
        if not self.number:
            last = ProductionOrder.objects.count()
            self.number = f'ЗП-{last + 1:03d}'
        super().save(*args, **kwargs)