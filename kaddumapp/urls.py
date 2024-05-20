from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('users.urls')),
]

handler404 = 'dashboard.views.not_found'  # This line tells Django to use your custom 404 handler
