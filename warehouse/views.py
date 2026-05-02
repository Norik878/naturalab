from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .models import Batch
from orders.models import ProductionOrder
from .models import Batch, Ingredient

@login_required
def dashboard(request):
    today = timezone.now().date()
    batches = Batch.objects.filter(status='available')

    context = {
        'active_orders':    ProductionOrder.objects.exclude(status__in=['done', 'cancelled']).count(),
        'total_batches':    batches.count(),
        'expiring_soon':    batches.filter(expiry_date__lte=today + timezone.timedelta(days=30)).count(),
        'expired':          batches.filter(expiry_date__lt=today).count(),
        'expiring_batches': batches.filter(expiry_date__lte=today + timezone.timedelta(days=30)).order_by('expiry_date')[:5],
        'recent_orders':    ProductionOrder.objects.all()[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
def batch_list(request):
    batches = Batch.objects.all().order_by('expiry_date')
    return render(request, 'warehouse/batch_list.html', {'batches': batches})

@login_required
def expiry_list(request):
    today = timezone.now().date()
    batches = Batch.objects.filter(status='available').order_by('expiry_date')
    context = {
        'batches':       batches,
        'ok_count':      batches.filter(expiry_date__gt=today + timezone.timedelta(days=30)).count(),
        'warning_count': batches.filter(expiry_date__lte=today + timezone.timedelta(days=30),
                                        expiry_date__gte=today).count(),
        'expired_count': batches.filter(expiry_date__lt=today).count(),
    }
    return render(request, 'warehouse/expiry_list.html', context)

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def user_list(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Пользователь {username} уже существует!')
            else:
                user = User.objects.create_user(username=username, password=password)
                group, _ = Group.objects.get_or_create(name='Сотрудник')
                user.groups.add(group)
                messages.success(request, f'Сотрудник {username} успешно добавлен!')
        return redirect('user-list')

    users = User.objects.filter(is_superuser=False).prefetch_related('groups')
    return render(request, 'warehouse/user_list.html', {'users': users})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Сотрудник {username} удалён.')
    return redirect('user-list')

@login_required
def batch_create(request):
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        lot_number    = request.POST.get('lot_number')
        quantity      = request.POST.get('quantity')
        received_at   = request.POST.get('received_at')
        expiry_date   = request.POST.get('expiry_date')

        if Batch.objects.filter(lot_number=lot_number).exists():
            messages.error(request, f'Партия с номером {lot_number} уже существует!')
        else:
            Batch.objects.create(
                ingredient_id=ingredient_id,
                lot_number=lot_number,
                quantity=quantity,
                received_at=received_at,
                expiry_date=expiry_date,
                status='available'
            )
            messages.success(request, f'Партия {lot_number} успешно добавлена!')
            return redirect('batch-list')

    return render(request, 'warehouse/batch_create.html', {'ingredients': ingredients})

@login_required
def ingredient_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        description = request.POST.get('description', '')

        if Ingredient.objects.filter(name=name).exists():
            messages.error(request, f'Сырьё "{name}" уже существует!')
        else:
            Ingredient.objects.create(name=name, unit=unit, description=description)
            messages.success(request, f'Сырьё "{name}" добавлено!')
            return redirect('batch-create')

    return render(request, 'warehouse/ingredient_create.html')