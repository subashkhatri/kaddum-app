from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('dairy_record', views.dairy_record, name='dairy_record'),
  path('daily_costing', views.daily_costing, name='daily_costing')
]