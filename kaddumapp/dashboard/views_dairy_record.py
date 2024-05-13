from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms_dairy_record import DairyRecordForm
from .models import DairyRecord
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.decorators import superuser_or_supervisor_required

@superuser_or_supervisor_required
def view_dairy_record(request, dairy_record_id):
    record = get_object_or_404(DairyRecord, pk=dairy_record_id)
    return render(request, 'dairy_record/view_dairy_record.html', {'record': record})

@superuser_or_supervisor_required
def all_dairy_record(request):
    draft_records_list = DairyRecord.objects.filter(is_draft=True).order_by('-created_date')
    completed_records_list = DairyRecord.objects.filter(is_draft=False).order_by('-created_date')
    paginator = Paginator(completed_records_list, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    dairy_records = paginator.get_page(page_number)
    return render(request, 'dairy_record/all_dairy_record.html', {'draft_records': draft_records_list, 'completed_records':completed_records_list})


@superuser_or_supervisor_required
def create_dairy_record(request):
    form_action = reverse('create_dairy_record')
    if request.method == 'POST':
        form = DairyRecordForm(request.POST)
        if form.is_valid():
          is_draft = request.POST.get('click-btn') == 'draft'
          dairy_record = form.save(commit=False)
          dairy_record.is_draft = is_draft
          dairy_record.save()
          messages.success(request, 'Dairy record created successfully.')
          return redirect('all_dairy_record')
    else:
        form = DairyRecordForm()
        return render(request, 'dairy_record/create_dairy_record.html', {'form': form, 'form_action': form_action})

@superuser_or_supervisor_required
def edit_dairy_record(request, dairy_record_id):
    form_action = reverse('edit_dairy_record', args=[dairy_record_id])
    record = get_object_or_404(DairyRecord, pk=dairy_record_id)
    if request.method == 'POST':
        form = DairyRecordForm(request.POST, instance=record)
        if form.is_valid():
          form.save()
          messages.success(request, 'Dairy record updated successfully.')
          return redirect('all_dairy_record')
    else:
        form = DairyRecordForm(instance=record)
        return render(request, 'dairy_record/edit_dairy_record.html', {'form': form, 'dairy_record': record, 'form_action': form_action})

@superuser_or_supervisor_required
def delete_dairy_record(request, dairy_record_id):
    record = get_object_or_404(DairyRecord, pk=dairy_record_id)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Dairy record deleted successfully.")
        return redirect('all_dairy_record')

    return render(request, 'dairy_record/confirm_delete.html', {'record': record})
