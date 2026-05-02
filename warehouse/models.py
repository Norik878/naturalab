from django.db import models

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Килограмм'),
        ('g',  'Грамм'),
        ('l',  'Литр'),
        ('ml', 'Миллилитр'),
    ]

    name        = models.CharField(max_length=200, verbose_name='Название')
    unit        = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name='Единица измерения')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Сырьё'
        verbose_name_plural = 'Сырьё'

    def __str__(self):
        return f'{self.name} ({self.get_unit_display()})'


class Batch(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('depleted',  'Израсходована'),
        ('expired',   'Просрочена'),
    ]

    ingredient   = models.ForeignKey(Ingredient, on_delete=models.PROTECT, verbose_name='Сырьё')
    lot_number   = models.CharField(max_length=50, unique=True, verbose_name='Номер партии')
    quantity     = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Остаток')
    received_at  = models.DateField(verbose_name='Дата поступления')
    expiry_date  = models.DateField(verbose_name='Срок годности')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        verbose_name = 'Партия сырья'
        verbose_name_plural = 'Партии сырья'
        ordering = ['expiry_date']

    def __str__(self):
        return f'{self.lot_number} — {self.ingredient.name}'

    @property
    def days_left(self):
        from django.utils import timezone
        delta = self.expiry_date - timezone.now().date()
        return delta.days

    @property
    def status_label(self):
        if self.days_left < 0:
            return 'expired'
        elif self.days_left <= 30:
            return 'warning'
        return 'ok'
    
class WriteOffLog(models.Model):
    batch       = models.ForeignKey(Batch, on_delete=models.PROTECT, verbose_name='Партия')
    order       = models.ForeignKey('orders.ProductionOrder', on_delete=models.PROTECT,
                                    verbose_name='Заказ')
    quantity    = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Списано')
    written_off_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата списания')
    written_off_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,
                                        null=True, blank=True, verbose_name='Кто списал')

    class Meta:
        verbose_name = 'Запись списания'
        verbose_name_plural = 'Журнал списания'
        ordering = ['-written_off_at']

    def __str__(self):
        return f'{self.batch.ingredient.name} - {self.quantity} ({self.order.number})'