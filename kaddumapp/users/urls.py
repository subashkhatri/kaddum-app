from django.urls import path
from . import views
import django.contrib.auth.views as auth_view


urlpatterns = [
    path('users/register_superuser/', views.register_superuser, name='register_superuser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employee_add/', views.employee_add, name='employees_add'),
    path('employee/<str:employee_id>/', views.employee_edit, name='employees_edit'),
    path('delete_employee/<str:username>/', views.delete_employee, name='delete_employee'),
]