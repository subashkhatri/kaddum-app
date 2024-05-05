from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),
  path('view_dairy_record/<str:dairy_record_id>/', views.view_dairy_record, name="view_dairy_record"),
  path('daily_costing', views.daily_costing, name='daily_costing'),
  path('all_daily_costing', views.all_daily_costing, name='all_daily_costing'),
]