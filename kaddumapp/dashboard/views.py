from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import DairyRecord
from django.utils.dateparse import parse_date
from django.contrib import messages
import logging
from datetime import date


logger = logging.getLogger(__name__)

def index(request):
  dairy_records = DairyRecord.objects.order_by('-record_created_date')
  return render(request, 'dashboard/index.html', {'records': dairy_records})

def all_dairy_record(request):
    dairy_records = DairyRecord.objects.order_by('-record_created_date')
    return render(request, 'dashboard/all_dairy_record.html', {'records': dairy_records})

def create_dairy_record(request):
    form_action = reverse('create_dairy_record')
    if request.method == 'POST':
        form_data = request.POST
        try:
            record_date = parse_date(form_data.get('record_date')) if form_data.get('record_date') else None
            new_record = DairyRecord(
                job_name=form_data.get('job_name', ''),
                client=form_data.get('client', ''),
                supervisor=form_data.get('supervisor', ''),
                record_date=record_date,
                record_shift=form_data.get('record_shift', ''),
                activity_discussion=form_data.get('activities_discussed', ''),
                safety_issue_discussion=form_data.get('safety_issues_discussed', ''),
                instruction_from_client=form_data.get('instruction_received', ''),
                visitor_on_site=form_data.get('site_visitor', ''),
                daily_progress_description=form_data.get('work_description', ''),
                record_comment=form_data.get('notes', ''),
                handover_note=form_data.get('handover_notes', ''),
                mobilised=int(form_data.get('mobilised', 0)),
                non_manual=int(form_data.get('non_manual', 0)),
                manual=int(form_data.get('manual', 0)),
                subcontractor=int(form_data.get('sub_contractor', 0)),
                environmental_incidents=int(form_data.get('environmental_incidents', 0)),
                near_misses=int(form_data.get('near_misses', 0)),
                first_aid=int(form_data.get('first_aid', 0)),
                medically_treated_injury=int(form_data.get('medically_treated_injury', 0)),
                loss_time_injury=int(form_data.get('loss_time_injury', 0)),
                record_created_date=date.today()
            )
            new_record.save()
            messages.success(request, 'Dairy record created successfully')
            return redirect('index')
        except Exception as e:
            logger.error('Error saving form data:', exc_info=True)
            messages.error(request, 'Error creating dairy record: {}'.format(e))
            return render(request, 'dashboard/create_dairy_record.html', {
                'form_action': form_action,
                'dairy_record': None
            }, status=400)
    else:
         return render(request, 'dashboard/create_dairy_record.html', {
            'form_action': form_action,
            'dairy_record': None
        })

def edit_dairy_record(request, dairy_record_id):
    dairy_record = get_object_or_404(DairyRecord, id=dairy_record_id)
    if request.method == 'POST':
        form_data = request.POST
        try:
            dairy_record.job_name = form_data.get('job_name', '')
            dairy_record.client = form_data.get('client', '')
            dairy_record.supervisor = form_data.get('supervisor', '')
            dairy_record.record_date = parse_date(form_data.get('record_date')) if form_data.get('record_date') else None
            dairy_record.record_shift = form_data.get('record_shift', '')
            dairy_record.activity_discussion = form_data.get('activities_discussed', '')
            dairy_record.safety_issue_discussion = form_data.get('safety_issues_discussed', '')
            dairy_record.instruction_from_client = form_data.get('instruction_received', '')
            dairy_record.visitor_on_site = form_data.get('site_visitor', '')
            dairy_record.daily_progress_description = form_data.get('work_description', '')
            dairy_record.record_comment = form_data.get('notes', '')
            dairy_record.handover_note = form_data.get('handover_notes', '')
            dairy_record.mobilised = int(form_data.get('mobilised', 0))
            dairy_record.non_manual = int(form_data.get('non_manual', 0))
            dairy_record.manual = int(form_data.get('manual', 0))
            dairy_record.subcontractor = int(form_data.get('sub_contractor', 0))
            dairy_record.environmental_incidents = int(form_data.get('environmental_incidents', 0))
            dairy_record.near_misses = int(form_data.get('near_misses', 0))
            dairy_record.first_aid = int(form_data.get('first_aid', 0))
            dairy_record.medically_treated_injury = int(form_data.get('medically_treated_injury', 0))
            dairy_record.loss_time_injury = int(form_data.get('loss_time_injury', 0))
            dairy_record.record_created_date = date.today()

            dairy_record.save()
            messages.success(request, 'Dairy record updated successfully')
            return redirect('index')
        except Exception as e:
            logger.error('Error updating form data:', exc_info=True)
            messages.error(request, 'Error updating dairy record: {}'.format(e))
            return render(request, 'dashboard/edit_dairy_record.html', {'dairy_record': dairy_record}, status=400)
    else:
        return render(request, 'dashboard/edit_dairy_record.html', {'dairy_record': dairy_record})
