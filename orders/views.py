from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProductionOrder

def order_list(request):
    orders = ProductionOrder.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_create(request):
    from products.models import Product
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity   = request.POST.get('quantity')
        due_date   = request.POST.get('due_date')
        notes      = request.POST.get('notes', '')
        order = ProductionOrder.objects.create(
            product_id=product_id,
            quantity=quantity,
            due_date=due_date,
            notes=notes,
            created_by=request.user,
        )
        messages.success(request, f'Заказ {order.number} успешно создан!')
        return redirect('order-list')
    products = Product.objects.all()
    return render(request, 'orders/order_create.html', {'products': products})

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .services import start_order

def order_detail(request, pk):
    order = get_object_or_404(ProductionOrder, pk=pk)
    recipe_items = []
    for item in order.product.recipe_items.all():
        recipe_items.append({
            'ingredient': item.ingredient,
            'quantity_per_unit': item.quantity_per_unit,
            'total': item.quantity_per_unit * order.quantity,
        })
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'recipe_items': recipe_items,
    })

def order_start(request, pk):
    order = get_object_or_404(ProductionOrder, pk=pk)
    if request.method == 'POST':
        try:
            start_order(order, user=request.user)
            messages.success(request, f'Заказ {order.number} запущен! Сырьё списано по FEFO.')
        except ValidationError as e:
            messages.error(request, e.message if hasattr(e, 'message') else str(e).strip("[]'"))
    return redirect('order-detail', pk=pk)

def order_done(request, pk):
    order = get_object_or_404(ProductionOrder, pk=pk)
    if request.method == 'POST':
        order.status = 'done'
        order.save()
        messages.success(request, f'Заказ {order.number} завершён!')
    return redirect('order-detail', pk=pk)