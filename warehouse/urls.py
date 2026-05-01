from django.urls import path
from . import views

urlpatterns = [
    path('batches/', views.batch_list, name='batch-list'),
    path('expiry/',  views.expiry_list, name='expiry-list'),
]