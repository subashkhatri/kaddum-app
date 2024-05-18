from django.shortcuts import render, get_object_or_404, redirect
from .models import CostTracking, DayTrackingEmployeeDetails, ResourceCost,DayTrackingEquipmentDetails
from django.core.paginator import Paginator
from .forms_costing import CostTrackingForm
from django.contrib import messages
from users.decorators import superuser_required

@superuser_required
def view_daily_costing(request, cost_tracking_id):
    # Fetch the specific instance of CostTracking using its ID
    costing = get_object_or_404(CostTracking, pk=cost_tracking_id)
    employee_details = DayTrackingEmployeeDetails.objects.filter(day_tracking_id__cost_tracking_id=costing).select_related('position_id', 'employee_id')
    equipment_details = DayTrackingEquipmentDetails.objects.filter(day_tracking_id__cost_tracking_id=costing)

    # Calculate day of the week from record_date
    day_of_week = costing.record_date.strftime('%A')

    # Calculate total_hours_indigenous and total_hours_local if not already calculated
    total_hours_indigenous = sum(emp.total_hours for emp in employee_details if emp.employee_id.is_indigenous)
    total_hours_local = sum(emp.total_hours for emp in employee_details if emp.employee_id.is_local)
    
    # Calculate percentages
    total_hours = sum(emp.total_hours for emp in employee_details)
    total_hours_indigenous_percentage = (total_hours_indigenous / total_hours * 100) if total_hours else 0
    total_hours_local_percentage = (total_hours_local / total_hours * 100) if total_hours else 0

    context = {
        'costing': costing,
        'employee_details': employee_details,
        'equipment_details': equipment_details,
        'day_of_week': day_of_week,
        'total_hours_indigenous': total_hours_indigenous,
        'total_hours_indigenous_percentage': total_hours_indigenous_percentage,
        'total_hours_local': total_hours_local,
        'total_hours_local_percentage': total_hours_local_percentage,
    }
    return render(request, 'costing/view_daily_costing.html', context)

@superuser_required
def edit_daily_costing(request, cost_tracking_id):
    # Fetch the specific instance of CostTracking using its ID
    instance = get_object_or_404(CostTracking, cost_tracking_id=cost_tracking_id)
    employee_details = DayTrackingEmployeeDetails.objects.filter(day_tracking_id__cost_tracking_id=instance).select_related('position_id', 'employee_id')
    equipment_details = DayTrackingEquipmentDetails.objects.filter(day_tracking_id__cost_tracking_id=instance)
    positions = ResourceCost.objects.filter(item_type='personel').order_by('item_name')

    if request.method == 'POST':
        form = CostTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            # Update the hour_rate for each employee
            for employee in employee_details:
                employee_id = str(employee.id)
                hour_rate = request.POST.get(f'rate_{employee_id}')
                new_position = request.POST.get(f'position_{employee_id}')
                new_position_id = ResourceCost.objects.get(resource_id=new_position)
                employee.hour_rate = hour_rate
                employee.confirmed_position_id = new_position_id
                employee.save()

            for equipment in equipment_details:
                new_item_rate = request.POST.get(f'equipment_rate_{equipment.id}')
                equipment.item_rate = float(new_item_rate) if new_item_rate else 0  # Convert to float or default to 0
                equipment.save()           

            if request.POST.get('action') == 'complete':
                form.instance.is_draft = False
                form.save()
                messages.success(request, 'Form completed successfully.')
            elif request.POST.get('action') == 'draft':
                form.instance.is_draft = True
                form.save()
                messages.success(request, 'Form saved as draft.')

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
        'instance': instance,  # This contains all the totals and percentages
    }

    return render(request, 'costing/edit_daily_costing.html', context)

@superuser_required
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
