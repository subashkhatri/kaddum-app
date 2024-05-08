from django.urls import path
from . import views
from . import views_costing
from . import views_dairy_record
from .views_day_tracking import create_day_tracking
from . import views_day_tracking
from . import project_views
from . import views_weekly_report

urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views_dairy_record.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views_dairy_record.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views_dairy_record.all_dairy_records, name='all_dairy_records'),
  path('view_dairy_record/<str:dairy_record_id>/', views_dairy_record.view_dairy_record, name="view_dairy_record"),
  path('delete_dairy_record/<str:dairy_record_id>/', views_dairy_record.delete_dairy_record, name='delete_dairy_record'),

  path('create_day_tracking/', views_day_tracking.create_day_tracking, name='create_day_tracking'),  
  path('all_day_tracking/', views_day_tracking.all_day_tracking, name='all_day_tracking'),
  path('edit_day_tracking/<str:day_tracking_id>/', views_day_tracking.edit_day_tracking, name='edit_day_tracking'),
  path('delete_day_tracking/<str:day_tracking_id>/', views_day_tracking.day_tracking_delete, name='day_tracking_delete'),

  path('all_daily_costing', views_costing.all_daily_costing, name='all_daily_costing'),
  path('edit_daily_costing/<str:cost_tracking_id>/', views_costing.edit_daily_costing, name='edit_daily_costing'),

  path('project_create/', project_views.project_create, name='project_create'),
  path('project_update/<str:project_no>/', project_views.project_update, name='project_update'),
  path('project_list', project_views.project_list, name='project_list'),
  path('project_delete_confirm/<str:project_no>/', project_views.project_delete, name='project_delete'),
  # path('project_view/<str:project_no>/', project_views.view_dairy_record, name="project_view"),  to be done

  path('view_weekly_report/', views_weekly_report.view_weekly_report, name='view_weekly_report'),
  path('all_weekly_report/', views_weekly_report.all_weekly_report, name='all_weekly_report'),

]

