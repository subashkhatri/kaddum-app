from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import DairyRecord
from django.utils.dateparse import parse_date
from django.contrib import messages
import logging
from datetime import date


logger = logging.getLogger(__name__)

def index(request):
  dairy_records = DairyRecord.objects.order_by('-record_created_date')
  return render(request, 'dashboard/index.html', {'records': dairy_records})


def dairy_record(request):
    if request.method == 'POST':
        logger.debug(request.POST)
        # Create a form instance and populate it with data from the request
        try:
            # Parse the date from the form input. This assumes the form sends the date in "YYYY-MM-DD" format.
            record_date = parse_date(request.POST['record_date']) if 'record_date' in request.POST and request.POST['record_date'] else None

            # Create a new DairyRecord instance with data from the form
            dairy_record = DairyRecord(
                job_name=request.POST.get('job_name', ''),
                client=request.POST.get('client', ''),
                supervisor=request.POST.get('supervisor', ''),
                record_date=record_date,
                record_shift=request.POST.get('record_shift', ''),
                activity_discussion=request.POST.get('activities_discussed', ''),
                safety_issue_discussion=request.POST.get('safety_issues_discussed', ''),
                instruction_from_client=request.POST.get('instruction_received', ''),
                visitor_on_site=request.POST.get('site_visitor', ''),
                daily_progress_description=request.POST.get('work_description', ''),
                record_comment=request.POST.get('notes', ''),
                handover_note=request.POST.get('handover_notes', ''),
                mobilised=int(request.POST.get('mobilised', 0)),
                non_manual=int(request.POST.get('non_manual', 0)),
                manual=int(request.POST.get('manual', 0)),
                subcontractor=int(request.POST.get('sub_contractor', 0)),
                environmental_incidents=int(request.POST.get('environmental_incidents', 0)),
                near_misses=int(request.POST.get('near_misses', 0)),
                first_aid=int(request.POST.get('first_aid', 0)),
                medically_treated_injury=int(request.POST.get('medically_treated_injury', 0)),
                loss_time_injury=int(request.POST.get('loss_time_injury', 0)),
                record_created_date=date.today()
            )

            # Save the DairyRecord instance to the database
            dairy_record.save()

            messages.success(request, 'Dairy record created successfully')
            return redirect('index')  # Redirect to a success page or another appropriate URL

        except Exception as e:
            logger.error('Error saving form data:', exc_info=True)
            messages.error(request, 'Error creating dairy record: {}'.format(e))
            return render(request, 'dashboard/dairy_record.html', status=400)

    else:
        # If not POST, render the page with the form
        return render(request, 'dashboard/dairy_record.html')
