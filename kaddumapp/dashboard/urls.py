from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create_dairy_record/', views.create_dairy_record, name='create_dairy_record'),
  path('edit_dairy_record/<int:dairy_record_id>/', views.edit_dairy_record, name='edit_dairy_record'),
  path('all_dairy_records', views.all_dairy_record, name='all_dairy_record'),

]