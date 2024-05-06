from django.shortcuts import render, get_object_or_404, redirect
from .models import CostTracking, Project, DayTracking, DayTrackingEmployeeDetails, ResourceCost,DayTrackingEquipmentDetails
from users.models import UserAccount
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime
from .costing_forms import CostTrackingForm
from django.urls import reverse
from django.contrib import messages



def edit_daily_costing(request, cost_tracking_id):
    instance = get_object_or_404(CostTracking, cost_tracking_id=cost_tracking_id)
    employee_details = DayTrackingEmployeeDetails.objects.filter(day_tracking_id__cost_tracking_id=instance).select_related('position_id', 'employee_id')
    positions = ResourceCost.objects.filter(item_type='personel').order_by('item_name')
    equipment_details = DayTrackingEquipmentDetails.objects.filter(day_tracking_id__cost_tracking_id=instance)

    if request.method == 'POST':
        form = CostTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            total_hours = 0
            total_amount = 0
            total_hours_indigenous = 0
            total_hours_local = 0

            # Calculate totals from employee details
            for employee in employee_details:
                employee_rate = request.POST.get(f'rate_{employee.id}', 0)
                total = float(employee_rate) * employee.total_hours
                total_hours += employee.total_hours
                total_amount += total
                if employee.employee_id.is_indigenous:
                    total_hours_indigenous += employee.total_hours
                if employee.employee_id.is_local:
                    total_hours_local += employee.total_hours

            # Optionally handle equipment details if they contribute to totals
            for equipment in equipment_details:
                equipment_rate = request.POST.get(f'rate_{equipment.id}', 0)
                total = float(equipment_rate) * equipment.total_hours


            # Save aggregated data to CostTracking instance
            instance.total_hours = total_hours
            instance.total_hours_local = total_hours_local
            instance.total_hours_indigenous = total_hours_indigenous
            instance.total_amount = total_amount
            instance.is_draft = False  # Assuming you want to finalize the entry
            form.save()
            print("saved")

            return redirect('all_daily_costing')
        else:
            # Handle form errors
            pass
    else:
        form = CostTrackingForm(instance=instance)

    return render(request, 'costing/edit_daily_costing.html', {
        'form': form,
        'employee_details': employee_details,
        'equipment_details': equipment_details,
        'positions': positions
    })



def all_daily_costing(request):
    draft_records_list = CostTracking.objects.filter(is_draft=True).order_by('-created_date')
    completed_records_list = CostTracking.objects.filter(is_draft=False).order_by('-created_date')
    paginator_draft = Paginator(draft_records_list, 10) 
    paginator_completed = Paginator(completed_records_list, 10)
    page_number_draft = request.GET.get('page_draft')
    page_number_completed = request.GET.get('page_completed')
    draft_records = paginator_draft.get_page(page_number_draft)
    completed_records = paginator_completed.get_page(page_number_completed)
    for record in draft_records:
        if record.record_date:
            record.day_of_week = record.record_date.strftime('%A')
    for record in completed_records:
        if record.record_date:
            record.day_of_week = record.record_date.strftime('%A')
    context = {
        'draft_records': draft_records,
        'completed_records': completed_records
    }
    return render(request, 'costing/all_daily_costing.html', context)


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