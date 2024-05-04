from django.urls import path
from . import views
from .views import check_day_tracking

urlpatterns = [
  path('', views.index, name='index'),
  path('dairy_record', views.dairy_record, name='dairy_record'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit_dairy_record/<int:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),
  path('daily_costing', views.daily_costing, name='daily_costing'),
  path('all_daily_costing', views.all_daily_costing, name='all_daily_costing'),
]