"""
URL configuration for gym_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),

    # Member Module
    path('members/', views.view_members, name='view_members'),
    path('add-member/', views.add_member, name='add_member'),
    path('edit-member/<int:id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:id>/', views.delete_member, name='delete_member'),
    path('member/<int:id>/', views.member_profile, name='member_profile'),
    path('member-stats/', views.member_stats, name='member_stats'),
]
