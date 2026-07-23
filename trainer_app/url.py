from django.urls import path
from . import views

urlpatterns = [
    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/add/', views.trainer_create, name='trainer_add'),
    path('trainers/<int:pk>/', views.trainer_detail, name='trainer_detail'),
    path('trainers/<int:pk>/edit/', views.trainer_update, name='trainer_edit'),
    path('trainers/<int:pk>/delete/', views.trainer_delete, name='trainer_delete'),  
]





