from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .forms_day_tracking import DayTrackingForm, DayTrackingEmployeeFormSet, DayTrackingEquipmentFormSet
from .models import DayTracking,  CostTracking, DayTrackingEmployeeDetails,DayTrackingEquipmentDetails, Project
from .models_resource_cost import ResourceCost
from users.models import UserAccount
from users.decorators import superuser_or_supervisor_required
import base64
import os
import datetime
import logging

logger = logging.getLogger(__name__)

@superuser_or_supervisor_required
def day_tracking_create(request):
    form_action = reverse('day_tracking_create')

    if request.method == 'POST':
        form = DayTrackingForm(request.POST)
        employee_formset = DayTrackingEmployeeFormSet(request.POST, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(request.POST, prefix='equipment')
        kaddum_sign_data = request.POST.get('kaddum_sign')
        client_sign_data = request.POST.get('client_sign')

        if form.is_valid() and employee_formset.is_valid() and equipment_formset.is_valid():
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
                day_tracking_instance.save()


                # Save signatures only if not a draft
                if not is_draft:
                    kaddum_sign_data = request.POST.get('kaddum_sign')
                    client_sign_data = request.POST.get('client_sign')
                    if kaddum_sign_data:
                        day_tracking_instance.kaddum_sign = kaddum_sign_data
                    if client_sign_data:
                        day_tracking_instance.client_sign = client_sign_data
                    day_tracking_instance.save()

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

def save_signature(image_data, filename):
    if image_data.startswith('data:image/svg+xml;base64,'):
        image_data = image_data.replace('data:image/svg+xml;base64,', '')

    try:
        image_data = base64.b64decode(image_data)
    except base64.binascii.Error as e:
        return

    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as f:
        f.write(image_data)

@superuser_or_supervisor_required
def day_tracking_update(request, day_tracking_id):
    form_action = reverse('day_tracking_update', args=[day_tracking_id])
    day_tracking_instance = get_object_or_404(DayTracking, day_tracking_id=day_tracking_id)
    record_PK = day_tracking_instance.day_tracking_id
    initial_purchase_order_no = day_tracking_instance.project_no.purchase_order_no if day_tracking_instance.project_no else "None"

    if request.method == 'POST':
        form = DayTrackingForm(request.POST, instance=day_tracking_instance)
        employee_formset = DayTrackingEmployeeFormSet(request.POST, instance=day_tracking_instance, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(request.POST, instance=day_tracking_instance, prefix='equipment')
        kaddum_sign_data = request.POST.get('kaddum_sign')
        client_sign_data = request.POST.get('client_sign')

        if form.is_valid() and employee_formset.is_valid() and equipment_formset.is_valid():
            with transaction.atomic():
                is_draft = request.POST.get('click-btn') == 'draft'
                day_tracking_instance = form.save(commit=False)
                day_tracking_instance.is_draft = is_draft
                day_tracking_instance.save()

                # Save the employee formset
                employee_formset.save(commit=True)


                # Save the equipment formset
                equipment_formset.save(commit=True)

                # Save signatures only if not a draft
                if not is_draft:
                    kaddum_sign_data = request.POST.get('kaddum_sign')
                    client_sign_data = request.POST.get('client_sign')
                    if kaddum_sign_data:
                        day_tracking_instance.kaddum_sign = kaddum_sign_data
                    if client_sign_data:
                        day_tracking_instance.client_sign = client_sign_data
                    day_tracking_instance.save()


                messages.success(request, "Day tracking record updated successfully.")
                return redirect('day_tracking_list')
        else:
            messages.error(request, "Form submission error. Please check the provided information.")

    else:
        form = DayTrackingForm(instance=day_tracking_instance)
        employee_formset = DayTrackingEmployeeFormSet(instance=day_tracking_instance, prefix='employee')
        equipment_formset = DayTrackingEquipmentFormSet(instance=day_tracking_instance, prefix='equipment')
        employee_formset.extra = 0

        if not equipment_formset.queryset.exists():
            equipment_formset = DayTrackingEquipmentFormSet(queryset=DayTrackingEquipmentDetails.objects.none(), prefix='equipment', extra=1)
        else:
            equipment_formset.extra = 0

    return render(request, 'day_tracking/day_tracking_update.html', {
        'form': form,
        'employee_formset': employee_formset,
        'equipment_formset': equipment_formset,
        'form_action': form_action,
        'record_PK':record_PK,
        'day_tracking_id': day_tracking_id,
        'initial_purchase_order_no':initial_purchase_order_no
    })

@superuser_or_supervisor_required
def day_tracking_list(request):

    draft_records_list = DayTracking.objects.filter(is_draft=True).order_by('-last_modification_date')
    query = request.GET.get('q', '').strip().lower()
    if query:
            try:
                # Attempt to parse the date if the query is a date string
                date_query = datetime.datetime.strptime(query, '%d/%m/%y').date()
            except ValueError:
                date_query = None

            completed_records_list = DayTracking.objects.filter(
                Q(is_draft=False) &
                (Q(day_tracking_id__icontains=query) |
                Q(record_date=date_query) |  # Exact date match
                Q(year_week__icontains=query) |
                Q(project_no__project_no__icontains=query) |
                Q(project_no__project_name__icontains=query) |
                Q(record_shift__icontains=query))  # This will handle date part search for last_modification_date
            ).order_by('-last_modification_date')
    else:
        completed_records_list = DayTracking.objects.filter(is_draft=False).order_by('-last_modification_date')

    paginator = Paginator(completed_records_list, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    completed_records_page  = paginator.get_page(page_number)
    return render(request, 'day_tracking/day_tracking_list.html', {
        'draft_records': draft_records_list,
        'completed_records':completed_records_page,
        'query': query,
        })

@superuser_or_supervisor_required
def day_tracking_delete(request, day_tracking_id):
    day_tracking_instance = get_object_or_404(DayTracking, pk=day_tracking_id)

    if request.method == 'POST':
        try:
            day_tracking_instance.delete()
            messages.success(request, f"DayTracking {day_tracking_instance.day_tracking_id} deleted successfully.")
        except ValidationError as e:
            messages.error(request, str(e))
        return redirect('day_tracking_list')

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
        'day_tracking_id': day_tracking_id
    })

def get_purchase_order(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        return JsonResponse({'purchase_order_no': project.purchase_order_no})
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

def get_position(request, employee_id):
    try:
        user = UserAccount.objects.get(username=employee_id)
        print(user.position_id.resource_id,user.position_id.item_name)
        return JsonResponse({'position_id': user.position_id.resource_id, 'position_name': user.position_id.item_name})

    except Project.DoesNotExist:
        print('Position not found')
        return JsonResponse({'error': 'Position not found'}, status=404)