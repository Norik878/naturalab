from django.shortcuts import render
from django.utils import timezone
from .models import Batch
from orders.models import ProductionOrder

def dashboard(request):
    today = timezone.now().date()
    batches = Batch.objects.filter(status='available')

    context = {
        'active_orders':   ProductionOrder.objects.exclude(status__in=['done','cancelled']).count(),
        'total_batches':   batches.count(),
        'expiring_soon':   batches.filter(expiry_date__lte=today + timezone.timedelta(days=30)).count(),
        'expired':         batches.filter(expiry_date__lt=today).count(),
        'expiring_batches': batches.filter(expiry_date__lte=today + timezone.timedelta(days=30)).order_by('expiry_date')[:5],
        'recent_orders':   ProductionOrder.objects.all()[:5],
    }
    return render(request, 'dashboard.html', context)

def batch_list(request):
    batches = Batch.objects.all().order_by('expiry_date')
    return render(request, 'warehouse/batch_list.html', {'batches': batches})

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