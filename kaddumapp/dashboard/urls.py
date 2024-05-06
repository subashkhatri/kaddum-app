from django.urls import path
from . import views, project_views


urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit-dairy_record/<str:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),
  path('view_dairy_record/<str:dairy_record_id>/', views.view_dairy_record, name="view_dairy_record"),
  path('delete_dairy_record/<str:dairy_record_id>/', views.delete_dairy_record, name='delete_dairy_record'),

  path('daily_costing', views.daily_costing, name='daily_costing'),
  path('all_daily_costing', views.all_daily_costing, name='all_daily_costing'),

  path('project_create/', project_views.project_create, name='project_create'),
  path('project_update/<str:project_no>/', project_views.project_update, name='project_update'),
  path('project_list', project_views.project_list, name='project_list'),
  path('project_delete/<str:project_no>/', project_views.project_delete, name='project_delete'),
  # path('project_view/<str:project_no>/', project_views.view_dairy_record, name="project_view"),  to be done
]