from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from warehouse.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('warehouse/', include('warehouse.urls')),
    path('orders/', include('orders.urls')),
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]