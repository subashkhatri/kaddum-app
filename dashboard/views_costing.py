from django.shortcuts import render, get_object_or_404, redirect
from .models import CostTracking, Project, DayTracking, DayTrackingEmployeeDetails, ResourceCost,DayTrackingEquipmentDetails
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q,Sum
from django.db import transaction
import datetime
from .forms_costing import CostTrackingForm
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
    record_PK = instance.cost_tracking_id

    if request.method == 'POST':
        form = CostTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            if form.is_valid():
                with transaction.atomic():  # Ensure all changes are made in a single transaction
                    form.save()  # Save changes to CostTracking
                    errors = []
                    # Update the hour_rate for each employee
                    for employee in employee_details:
                        employee_id = str(employee.id)
                        hour_rate = request.POST.get(f'rate_{employee_id}')
                        if float(hour_rate) < 0:
                            errors.append(f"Employee: {employee.employee_id.full_name} hour rate is incorrect.")
                        else:
                            new_position = request.POST.get(f'position_{employee_id}')
                            new_position_id = ResourceCost.objects.get(resource_id=new_position)
                            employee.hour_rate = hour_rate
                            employee.confirmed_position_id = new_position_id
                            employee.save()

                    for equipment in equipment_details:
                        equipment_id = str(equipment.id)
                        item_rate = request.POST.get(f'equipment_rate_{equipment_id}', 0)
                        if float(item_rate) < 0:
                            errors.append(f"Equipment: {equipment.resource_id.item_name} day rate is incorrect.")
                        else:
                            equipment.item_rate = float(item_rate)
                            equipment.save()

                    if request.POST.get('action') == 'complete':
                        form.instance.is_draft = False
                        form.save()
                        messages.success(request, 'Form completed successfully.')
                    elif request.POST.get('action') == 'draft':
                        form.instance.is_draft = True
                        form.save()

                    if not errors:
                        # Call the method to update CostTracking statistics
                        _update_cost_tracking_statistics(instance)
                        messages.success(request, 'Cost tracking and associated details updated successfully.')
                        return redirect('all_daily_costing')
                    else:
                        for error in errors:
                            messages.error(request, error)

                messages.success(request, 'Cost tracking and associated details updated successfully.')
                return redirect('all_daily_costing')
        else:
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
    draft_records_list = CostTracking.objects.filter(is_draft=True).order_by('-last_modification_date')
    query = request.GET.get('q', '').strip().lower()
    if query:
        try:
            # Attempt to parse the query as a date
            date_query = datetime.datetime.strptime(query, '%d/%m/%y').date()
        except ValueError:
            date_query = None

        completed_records_list = CostTracking.objects.filter(
        Q(is_draft=False) &
        (Q(cost_tracking_id__icontains=query) |
        Q(record_date=date_query) |  # Exact date match
        Q(year_week__icontains=query) |
        Q(project_no__project_no__icontains=query) |
        Q(project_no__project_name__icontains=query) |
        Q(last_modification_date__icontains=query))
        ).order_by('-created_date')
    else:
        completed_records_list = CostTracking.objects.filter(is_draft=False).order_by('-last_modification_date')

    paginator = Paginator(completed_records_list, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    completed_records_page  = paginator.get_page(page_number)

    context = {
        'draft_records': draft_records_list,
        'completed_records': completed_records_page
    }
    return render(request, 'costing/all_daily_costing.html', context)


def _update_cost_tracking_statistics(cost_tracking_instance):
    if cost_tracking_instance:
        # Aggregate various totals from DayTracking records associated with this CostTracking instance
        day_tracking_aggregates = DayTracking.objects.filter(cost_tracking_id=cost_tracking_instance).aggregate(
            total_hours_employee=Sum('total_hours_employee'),
            total_hours_employee_local=Sum('total_hours_employee_local'),
            total_hours_employee_indigenous=Sum('total_hours_employee_indigenous'),
            total_amount_employee=Sum('total_amount_employee'),
            total_hours_equipment=Sum('total_hours_equipment'),
            total_amount_equipment=Sum('total_amount_equipment')
        )

        # Extract aggregates and provide defaults if None
        total_hours_employee = day_tracking_aggregates.get('total_hours_employee', 0) or 0
        total_hours_employee_local = day_tracking_aggregates.get('total_hours_employee_local', 0) or 0
        total_hours_employee_indigenous = day_tracking_aggregates.get('total_hours_employee_indigenous', 0) or 0
        total_amount_employee = day_tracking_aggregates.get('total_amount_employee', 0) or 0
        total_hours_equipment = day_tracking_aggregates.get('total_hours_equipment', 0) or 0
        total_amount_equipment = day_tracking_aggregates.get('total_amount_equipment', 0) or 0

        # Calculate percentages for local and indigenous hours if total hours employee is not zero
        local_percentage = (total_hours_employee_local / total_hours_employee * 100) if total_hours_employee else 0
        indigenous_percentage = (total_hours_employee_indigenous / total_hours_employee * 100) if total_hours_employee else 0

        # Update the CostTracking instance with these aggregates
        cost_tracking_instance.total_hours_employee = total_hours_employee
        cost_tracking_instance.total_hours_employee_local = total_hours_employee_local
        cost_tracking_instance.total_hours_employee_indigenous = total_hours_employee_indigenous
        cost_tracking_instance.total_amount_employee = total_amount_employee
        cost_tracking_instance.total_hours_equipment = total_hours_equipment
        cost_tracking_instance.total_amount_equipment = total_amount_equipment
        cost_tracking_instance.total_hours_employee_local_percentage = local_percentage
        cost_tracking_instance.total_hours_employee_indigenous_percentage = indigenous_percentage
        cost_tracking_instance.last_modification_date = datetime.datetime.now()

        # Save the updated CostTracking instance
        cost_tracking_instance.save()
