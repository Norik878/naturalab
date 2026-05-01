from django.contrib import admin
from django.urls import path, include
from warehouse.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('warehouse/', include('warehouse.urls')),
    path('orders/', include('orders.urls')),
]