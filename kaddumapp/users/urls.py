from django.urls import path
from . import views
import django.contrib.auth.views as auth_view


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('employees/', views.employees_list, name='employees'),
    path('employees_add/', views.employees_add, name='employees_add'),
]