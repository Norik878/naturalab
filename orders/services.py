from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from warehouse.models import Batch

@transaction.atomic
def start_order(order):
    """Запускает заказ и списывает сырьё по алгоритму FEFO."""
    recipe_items = order.product.recipe_items.all()

    if not recipe_items:
        raise ValidationError('У продукта нет рецептуры — добавьте состав в Admin.')

    for item in recipe_items:
        needed = item.quantity_per_unit * order.quantity

        # FEFO: берём партии с ближайшим сроком годности первыми
        batches = Batch.objects.filter(
            ingredient=item.ingredient,
            status='available',
            expiry_date__gte=timezone.now().date()
        ).order_by('expiry_date')

        remaining = needed
        for batch in batches:
            if remaining <= 0:
                break
            take = min(batch.quantity, remaining)
            batch.quantity -= take
            if batch.quantity == 0:
                batch.status = 'depleted'
            batch.save()
            remaining -= take

        if remaining > 0:
            raise ValidationError(
                f'Недостаточно сырья: {item.ingredient.name} '
                f'(не хватает {remaining} {item.ingredient.get_unit_display()})'
            )

    order.status = 'in_progress'
    order.save()