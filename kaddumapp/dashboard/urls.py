from django.urls import path
from . import views
from . import views_costing
from . import views_dairy_record
from . import views_day_tracking
from . import views_project
from . import views_weekly_report
from . import views_resource



urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views_dairy_record.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views_dairy_record.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_record', views_dairy_record.all_dairy_record, name='all_dairy_record'),
  path('view_dairy_record/<str:dairy_record_id>/', views_dairy_record.view_dairy_record, name="view_dairy_record"),
  path('delete_dairy_record/<str:dairy_record_id>/', views_dairy_record.delete_dairy_record, name='delete_dairy_record'),

  path('day_tracking_create/', views_day_tracking.day_tracking_create, name='day_tracking_create'),  
  path('day_tracking_list/', views_day_tracking.day_tracking_list, name='day_tracking_list'),
  path('day_tracking_update/<str:day_tracking_id>/', views_day_tracking.day_tracking_update, name='day_tracking_update'),
  path('day_tracking_delete/<str:day_tracking_id>/', views_day_tracking.day_tracking_delete, name='day_tracking_delete'),
  path('view_day_tracking/<str:day_tracking_id>/', views_day_tracking.view_day_tracking, name='view_day_tracking'),



  path('all_daily_costing', views_costing.all_daily_costing, name='all_daily_costing'),
  path('edit_daily_costing/<str:cost_tracking_id>/', views_costing.edit_daily_costing, name='edit_daily_costing'),
  path('view_daily_costing/<str:cost_tracking_id>/', views_costing.view_daily_costing, name='view_daily_costing'),


  path('project_create/', views_project.project_create, name='project_create'),
  path('project_update/<str:project_no>/', views_project.project_update, name='project_update'),
  path('project_list', views_project.project_list, name='project_list'),
  path('project_delete_confirm/<str:project_no>/', views_project.project_delete, name='project_delete'),

  path('all_weekly_report/', views_weekly_report.all_weekly_report, name='all_weekly_report'),
  path('view_weekly_report/<int:report_id>/', views_weekly_report.view_weekly_report, name='view_weekly_report'),

  path('resource_cost/', views_resource.resource_cost_list, name='resource_cost_list'),
  path('resource_cost/create/', views_resource.create_resource_cost, name='create_resource_cost'),
  path('edit_resource_cost/<int:resource_id>/', views_resource.edit_resource_cost, name='edit_resource_cost'),
  path('resource_cost/delete/<int:resource_id>/', views_resource.delete_resource_cost, name='delete_resource_cost'),
]

