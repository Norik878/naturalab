from django.urls import path
from . import views

urlpatterns = [
    path('batches/',              views.batch_list,        name='batch-list'),
    path('batches/create/',       views.batch_create,      name='batch-create'),
    path('expiry/',               views.expiry_list,       name='expiry-list'),
    path('ingredients/create/',   views.ingredient_create, name='ingredient-create'),
    path('users/',                views.user_list,         name='user-list'),
    path('users/<int:pk>/delete/', views.user_delete,      name='user-delete'),
    path('writeoff/', views.writeoff_log, name='writeoff-log'),
    path('reports/', views.reports, name='reports'),
]