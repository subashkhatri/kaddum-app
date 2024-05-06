from django.urls import path
from . import views
import django.contrib.auth.views as auth_view


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employee_create/', views.employee_create, name='employee_create'),
    path('employee/<str:employee_id>/', views.employee_update, name='employees_edit'),
]