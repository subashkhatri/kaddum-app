from django.urls import path
from . import views
from .views import check_day_tracking

urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),
<<<<<<< Updated upstream
  path('view_dairy_record/<str:dairy_record_id>/', views.view_dairy_record, name="view_dairy_record"),
  path('delete_dairy_record/<str:dairy_record_id>/', views.delete_dairy_record, name='delete_dairy_record'),
  path('daily_costing', views.daily_costing, name='daily_costing'),
=======
  path('create_daily_costing', views.create_daily_costing, name='create_daily_costing'),
>>>>>>> Stashed changes
  path('all_daily_costing', views.all_daily_costing, name='all_daily_costing'),
]