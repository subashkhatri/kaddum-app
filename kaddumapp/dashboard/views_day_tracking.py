from django.db import transaction
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms_day_tracking import DayTrackingForm, DayTrackingEmployeeFormset, DayTrackingEquipmentFormset
from .models import DayTracking, DayTrackingEmployeeDetails, DayTrackingEquipmentDetails, Project
from django.core.paginator import Paginator
import logging
from django.contrib import messages
from django.forms import modelformset_factory

logger = logging.getLogger(__name__)

@transaction.atomic
def create_day_tracking(request):
    form_action = reverse ('create_day_tracking')
    if request.method == 'POST':
        form = DayTrackingForm(request.POST, request.FILES)
        employee_formset = DayTrackingEmployeeFormset(request.POST, prefix='employees', queryset=DayTrackingEmployeeDetails.objects.none())
        equipment_formset = DayTrackingEquipmentFormset(request.POST, prefix='equipment', queryset=DayTrackingEquipmentDetails.objects.none())

        if form.is_valid() and employee_formset.is_valid() and equipment_formset.is_valid():
            day_tracking = form.save()
            employee_formset.instance = day_tracking
            equipment_formset.instance = day_tracking
            employee_formset.save()
            equipment_formset.save()

            messages.success(request, "Day tracking record created successfully.")
            return redirect('all_day_tracking') 
        else:
            return render(request, 'day_tracking/create_day_tracking.html', {
                'form': form,
                'employee_formset': employee_formset,
                'equipment_formset': equipment_formset
            })
    else:
        form = DayTrackingForm()
        employee_formset = DayTrackingEmployeeFormset(prefix='employees', queryset=DayTrackingEmployeeDetails.objects.none())
        equipment_formset = DayTrackingEquipmentFormset(prefix='equipment', queryset=DayTrackingEquipmentDetails.objects.none())
        return render(request, 'day_tracking/create_day_tracking.html', {
            'form': form,
            'employee_formset': employee_formset,
            'equipment_formset': equipment_formset
        })



def all_day_tracking(request):
    draft_records_list = DayTracking.objects.filter(is_draft=True).order_by('-created_date')
    completed_records_list = DayTracking.objects.filter(is_draft=False).order_by('-created_date')
    # Fetch all records from the DayTracking model
    records = DayTracking.objects.all().select_related('project_no')
    return render(request, 'day_tracking/all_day_tracking.html', {'draft_records': draft_records_list, 'completed_records':completed_records_list})

def edit_day_tracking(request, day_tracking_id):
    record = get_object_or_404(DayTracking, pk=day_tracking_id)
    if request.method == 'POST':
        form = DayTrackingForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('all_day_tracking')
    else:
        form = DayTrackingForm(instance=record)

    return render(request, 'day_tracking/edit_day_tracking.html', {'form': form, 'record': record})

def day_tracking_delete(request, day_tracking_id):
    day_tracking = get_object_or_404(DayTracking, pk=day_tracking_id)
    try:
        # Manually delete related equipment details first
        DayTrackingEquipmentDetails.objects.filter(day_tracking_id=day_tracking).delete()
        DayTrackingEmployeeDetails.objects.filter(day_tracking_id=day_tracking).delete()
        day_tracking.delete()
        messages.success(request, "Day tracking record and all associated equipment details deleted successfully.")
        return redirect('all_day_tracking')
    except Exception as e:
        messages.error(request, f"Failed to delete day tracking record: {str(e)}")
        return redirect('all_day_tracking')


