from django.shortcuts import render, get_object_or_404, redirect
from .models import CostTracking, Project, DayTracking, DayTrackingEmployeeDetails, ResourceCost,DayTrackingEquipmentDetails
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime
from .forms_costing import CostTrackingForm
from django.contrib import messages
from users.decorators import superuser_required

@superuser_required
def view_daily_costing(request, cost_tracking_id):
    costing = get_object_or_404(CostTracking, pk=cost_tracking_id)
    context = {
        'costing': costing,
    }
    return render(request, 'costing/view_daily_costing.html', context)

@superuser_required
def edit_daily_costing(request, cost_tracking_id):
    # Fetch the specific instance of CostTracking using its ID
    instance = get_object_or_404(CostTracking, cost_tracking_id=cost_tracking_id)
    employee_details = DayTrackingEmployeeDetails.objects.filter(day_tracking_id__cost_tracking_id=instance).select_related('position_id', 'employee_id')
    equipment_details = DayTrackingEquipmentDetails.objects.filter(day_tracking_id__cost_tracking_id=instance)
    positions = ResourceCost.objects.filter(item_type='personel').order_by('item_name')
    record_PK = instance.cost_tracking_id

    # Calculate the total hours and total amount for the instance
    # instance.calculate_total()
    # instance.save()

    if request.method == 'POST':
        form = CostTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            if request.POST.get('action') == 'complete':
                form.instance.is_draft = False
                form.save()
                messages.success(request, 'Form completed successfully.')
            elif request.POST.get('action') == 'draft':
                form.instance.is_draft = True
                form.save()
                messages.success(request, 'Form saved as draft.')

            # Update the hour_rate for each employee
            for employee in employee_details:
                employee_id = str(employee.id)
                hour_rate = request.POST.get(f'rate_{employee_id}')
                employee.hour_rate = hour_rate
                employee.save()

            for equipment in equipment_details:
                item_rate = request.POST.get(f'equipment_rate_{equipment.id}')
                equipment.item_rate = float(item_rate) if item_rate else 0  # Convert to float or default to 0
                equipment.save()

            return redirect('all_daily_costing')
        else:
            print(form.errors)
            messages.error(request, 'Please correct the form errors.')

    else:
        form = CostTrackingForm(instance=instance)

    context = {
        'form': form,
        'employee_details': employee_details,
        'equipment_details': equipment_details,
        'positions': positions,
        'instance': instance,  # This contains all the totals and percentages,
        'record_PK':record_PK,
    }

    return render(request, 'costing/edit_daily_costing.html', context)

@superuser_required
def all_daily_costing(request):
    draft_records_list = CostTracking.objects.filter(is_draft=True).order_by('-created_date')
    completed_records_list = CostTracking.objects.filter(is_draft=False).order_by('-created_date')

    paginator = Paginator(completed_records_list, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    completed_records_page  = paginator.get_page(page_number)

    context = {
        'draft_records': draft_records_list,
        'completed_records': completed_records_page
    }
    return render(request, 'costing/all_daily_costing.html', context)

@superuser_required
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