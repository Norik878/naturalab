from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Product, RecipeItem
from warehouse.models import Ingredient

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def product_list(request):
    products = Product.objects.prefetch_related('recipe_items__ingredient').all()
    return render(request, 'products/product_list.html', {'products': products})

@admin_required
def product_create(request):
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        name        = request.POST.get('name')
        description = request.POST.get('description', '')

        if Product.objects.filter(name=name).exists():
            messages.error(request, f'Продукт "{name}" уже существует!')
        else:
            product = Product.objects.create(name=name, description=description)

            ingredient_ids = request.POST.getlist('ingredient_id')
            quantities     = request.POST.getlist('quantity')

            for ing_id, qty in zip(ingredient_ids, quantities):
                if ing_id and qty:
                    try:
                        RecipeItem.objects.create(
                            product=product,
                            ingredient_id=ing_id,
                            quantity_per_unit=qty
                        )
                    except Exception:
                        pass

            messages.success(request, f'Продукт "{name}" успешно создан!')
            return redirect('product-list')

    return render(request, 'products/product_create.html', {'ingredients': ingredients})

@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Продукт "{name}" удалён.')
    return redirect('product-list')