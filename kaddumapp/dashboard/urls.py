from django.urls import path
from . import views
from . import views_costing

urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),
  path('view_dairy_record/<str:dairy_record_id>/', views.view_dairy_record, name="view_dairy_record"),
  path('delete_dairy_record/<str:dairy_record_id>/', views.delete_dairy_record, name='delete_dairy_record'),
  path('all_daily_costing', views_costing.all_daily_costing, name='all_daily_costing'),
  path('edit_daily_costing/<str:cost_tracking_id>/', views_costing.edit_daily_costing, name='edit_daily_costing'),
]