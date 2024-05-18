from django.urls import path
from . import views
import django.contrib.auth.views as auth_view


urlpatterns = [
    path('users/register_superuser/', views.register_superuser, name='register_superuser'), 
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employee_create/', views.employee_add, name='employees_create'),
    path('employee_edit/<str:username>/', views.employee_edit, name='employees_edit'),
    path('employee_delete/<str:username>/', views.employee_delete, name='employee_delete'),
]