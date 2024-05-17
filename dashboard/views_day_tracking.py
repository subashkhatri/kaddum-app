from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError

from .forms_day_tracking import DayTrackingForm, DayTrackingEmployeeFormSet, DayTrackingEquipmentFormSet
from .models import DayTracking,  CostTracking, DayTrackingEmployeeDetails,DayTrackingEquipmentDetails

from users.decorators import superuser_or_supervisor_required
import logging

logger = logging.getLogger(__name__)

@superuser_or_supervisor_required
def day_tracking_create(request):
    form_action = reverse('day_tracking_create')

    if request.method == 'POST':
        form = DayTrackingForm(request.POST)
        employee_formset = DayTrackingEmployeeFormSet(request.POST, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(request.POST, prefix='equipment')


        if form.is_valid() and employee_formset.is_valid() and equipment_formset.is_valid():
            if not any(employee_formset.cleaned_data):
                messages.error(request, "Please add at least one employee.")
                return render(request, 'day_tracking/day_tracking_create.html', {'form': form, 'employee_formset': employee_formset, 'equipment_formset': equipment_formset})
            
            with transaction.atomic():
                is_draft = request.POST.get('click-btn') == 'draft'
                day_tracking_instance = form.save(commit=False)
                day_tracking_instance.is_draft = is_draft
                day_tracking_instance.save()

                # Save the employee formset
                for employee_form in employee_formset:
                    if employee_form.cleaned_data:
                        employee_detail = employee_form.save(commit=False)
                        employee_detail.day_tracking_id = day_tracking_instance
                        employee_detail.save()
                
                # Save the equipment formset
                for equipment_form in equipment_formset:
                    if equipment_form.cleaned_data:
                        equipment_detail = equipment_form.save(commit=False)
                        equipment_detail.day_tracking_id = day_tracking_instance
                        equipment_detail.save()

            messages.success(request, "Day tracking record created successfully.")
            return redirect('day_tracking_list')
        else:
            messages.error(request, "Form submission error. Please check the provided information.")

    else:
        form = DayTrackingForm()
        employee_formset = DayTrackingEmployeeFormSet(prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(prefix='equipment')

    return render(request, 'day_tracking/day_tracking_create.html', {
        'form': form,
        'employee_formset': employee_formset,
        'equipment_formset': equipment_formset,
        'form_action': form_action,
    })

@superuser_or_supervisor_required
def day_tracking_update(request, day_tracking_id):
    form_action = reverse('day_tracking_update', args=[day_tracking_id])
    day_tracking_instance = get_object_or_404(DayTracking, day_tracking_id=day_tracking_id)
    record_PK = day_tracking_instance.day_tracking_id

    if request.method == 'POST':
        form = DayTrackingForm(request.POST, instance=day_tracking_instance)
        employee_formset = DayTrackingEmployeeFormSet(request.POST, instance=day_tracking_instance, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(request.POST, instance=day_tracking_instance, prefix='equipment')


        if form.is_valid() and employee_formset.is_valid() and equipment_formset.is_valid():
            if not any(employee_formset.cleaned_data):
                messages.error(request, "Please add at least one employee.")
                return render(request, 'day_tracking/day_tracking_update.html', {'form': form, 'employee_formset': employee_formset, 'equipment_formset': equipment_formset})
                
            with transaction.atomic():
                is_draft = request.POST.get('click-btn') == 'draft'
                day_tracking_instance = form.save(commit=False)
                day_tracking_instance.is_draft = is_draft
                day_tracking_instance.save()

                # Save the employee formset
                employee_formset.save()

                # Save the equipment formset
                equipment_formset.save()

                messages.success(request, "Day tracking record updated successfully.")
                return redirect('day_tracking_list')
        else:
            messages.error(request, "Form submission error. Please check the provided information.")

    else:
        form = DayTrackingForm(instance=day_tracking_instance)
        employee_formset = DayTrackingEmployeeFormSet(instance=day_tracking_instance, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(instance=day_tracking_instance, prefix='equipment')
        extra_value = 1 if day_tracking_instance is None else 0
        employee_formset.extra = extra_value
        equipment_formset.extra = extra_value

    return render(request, 'day_tracking/day_tracking_update.html', {
        'form': form,
        'employee_formset': employee_formset,
        'equipment_formset': equipment_formset,
        'form_action': form_action,
        'record_PK':record_PK
    })

@superuser_or_supervisor_required
def day_tracking_list(request):
    draft_records_list = DayTracking.objects.filter(is_draft=True).order_by('-created_date')
    completed_records_list = DayTracking.objects.filter(is_draft=False).order_by('-created_date')
    # Fetch all records from the DayTracking model
    records = DayTracking.objects.all().select_related('project_no')
    return render(request, 'day_tracking/day_tracking_list.html', {'draft_records': draft_records_list, 'completed_records':completed_records_list})

@superuser_or_supervisor_required
def day_tracking_delete(request, day_tracking_id):
    day_tracking_instance = get_object_or_404(DayTracking, pk=day_tracking_id)

    if request.method == 'POST':
        try:
            day_tracking_instance.delete()
            messages.success(request, f"DayTracking {day_tracking_instance.day_tracking_id} deleted successfully.")            
        except ValidationError as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(reverse('day_tracking_list'))

    return render(request, 'day_tracking/day_tracking_delete.html', {'record': day_tracking_instance})

@superuser_or_supervisor_required
def day_tracking_view(request, day_tracking_id):
    day_tracking = get_object_or_404(DayTracking, pk=day_tracking_id)
    employee_formset = DayTrackingEmployeeDetails.objects.all().filter(day_tracking_id=day_tracking)
    equipment_formset = DayTrackingEquipmentDetails.objects.all().filter(day_tracking_id=day_tracking)
    
    return render(request, 'day_tracking/day_tracking_view.html', {
        'day_tracking': day_tracking,
        'employee_formset': employee_formset,
        'equipment_formset': equipment_formset,
    })

