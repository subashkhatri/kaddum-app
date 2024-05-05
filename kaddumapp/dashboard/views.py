from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .dairy_record_forms import DairyRecordForm
from .models import DairyRecord, CostTracking, Project, DayTracking, DayTrackingEmployeeDetails, ResourceCost
from users.models import UserAccount
from django.utils.dateparse import parse_date
from django.contrib import messages
import logging
from django.core.paginator import Paginator

from datetime import date
from django.http import JsonResponse
import datetime

logger = logging.getLogger(__name__)

def index(request):
  dairy_records = DairyRecord.objects.order_by('-created_date')
  return render(request, 'dashboard/index.html', {'records': dairy_records})

def dairy_record(request):
  return render(request, 'dashboard/dairy_record.html')

def all_dairy_record(request):
    records_list = DairyRecord.objects.order_by('-created_date')
    paginator = Paginator(records_list, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    dairy_records = paginator.get_page(page_number)
    return render(request, 'dashboard/all_dairy_record.html', {'records': dairy_records})

def create_dairy_record(request):
    form_action = reverse('create_dairy_record')
    if request.method == 'POST':
        form = DairyRecordForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request, 'Dairy record created successfully.')
          return redirect('index')
    else:
        form = DairyRecordForm()
        return render(request, 'dashboard/create_dairy_record.html', {'form': form, 'form_action': form_action})

def edit_dairy_record(request, dairy_record_id):
    form_action = reverse('edit_dairy_record', args=[dairy_record_id])
    record = get_object_or_404(DairyRecord, pk=dairy_record_id)
    if request.method == 'POST':
        form = DairyRecordForm(request.POST, instance=record)
        if form.is_valid():
          form.save()
          messages.success(request, 'Dairy record updated successfully.')
          return redirect('index')
    else:
        form = DairyRecordForm(instance=record)
        return render(request, 'dashboard/edit_dairy_record.html', {'form': form, 'dairy_record': record, 'form_action': form_action})


def daily_costing(request):
    projects = Project.objects.filter(is_active=True).order_by('project_name')
    employee_names = UserAccount.objects.filter(is_active=True).values_list('full_name', flat=True).distinct()
    positions = ResourceCost.objects.filter(item_type='personel').values_list('item_name', flat=True).distinct()

    return render(request, 'costing/daily_costing.html', {
        'projects': projects,
        'employee_names': employee_names,
        'positions': positions
    })

def all_daily_costing(request):
    daily_costing = CostTracking.objects.order_by('-created_date')
    return render(request, 'costing/all_daily_costing.html', {'records': daily_costing})


def check_day_tracking(request):
    project_name = request.GET.get('projectName')
    date_input = request.GET.get('date')

    try:
        input_date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid date format'})

    project = Project.objects.filter(project_name=project_name, is_active=True).first()
    if not project:
        return JsonResponse({'success': False, 'message': 'Project not found or not active'})

    day_tracking = DayTracking.objects.filter(record_date=input_date, project_no=project.project_no).first()
    if not day_tracking:
        return JsonResponse({'success': False, 'message': 'No matching day tracking record found'})

    employee_details = DayTrackingEmployeeDetails.objects.filter(day_tracking_no=day_tracking.id).values(
        'employee_name', 'position', 'item_rate', 'total_hours'
    )
    employee_data = [
        {
            'name': emp['employee_name'],
            'position': emp['position'],
            'total_hours': emp['total_hours'],
            'rate': emp['item_rate'],
            'total_amount': float(emp['item_rate']) * float(emp['total_hours']),
            'indigenous': '⭕',  # Assuming all are indigenous for example
            'local': ''  # Assuming all are non-local for example
        }
        for emp in employee_details
    ]

    return JsonResponse({
        'success': True,
        'employees': employee_data
    })