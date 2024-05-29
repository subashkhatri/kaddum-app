from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from .models import DairyRecord, Project, CostTracking, WeeklyReportList
import datetime
from users.decorators import superuser_or_supervisor_required

@superuser_or_supervisor_required
def all_weekly_report(request):
    query = request.GET.get('q', '').strip().lower()

    if query:
        try:
            # Attempt to parse the query as a date
            date_query = datetime.datetime.strptime(query, '%d/%m/%y').date()
        except ValueError:
            date_query = None

        new_reports = WeeklyReportList.objects.filter(
            Q(year_week__icontains=query) |
            Q(project_no__project_no__icontains=query) |
            Q(project_no__project_name__icontains=query) |
            Q(start_date=date_query) |
            Q(end_date=date_query) |
            Q(created_date__date=date_query)  # Exact date match
        ).order_by('-created_date')
    else:
        new_reports = WeeklyReportList.objects.all().order_by('-created_date')

    projects = Project.objects.all().order_by('project_no')
    weeks = CostTracking.objects.all().values_list('year_week', flat=True).distinct()
    unique_projects = {(project.project_no, project.project_name) for project in projects}
    unique_weeks = sorted(set(weeks), reverse=True)

    paginator = Paginator(new_reports, 10)  # Show 10 reports per page.
    page_number = request.GET.get('page')
    new_reports_page = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'create_report' in request.POST:
            project_no = request.POST.get('project_no')
            year_week = request.POST.get('year_week')
            project_instance = Project.objects.get(project_no=project_no)

            # Check if a report already exists for the specified project and week
            if WeeklyReportList.objects.filter(project_no=project_instance, year_week=year_week).exists():
                messages.error(request, "A report for this project and week already exists. Please delete the existing report if you wish to create a new one.")
            elif not CostTracking.objects.filter(project_no=project_no, year_week=year_week, is_draft=False).exists():
                messages.error(request, "No completed cost tracking records exist for the given project and week.")
            else:
                dairy_records = DairyRecord.objects.filter(project_no=project_no, year_week=year_week, is_draft=False)

                if dairy_records.exists():
                    aggregates = dairy_records.aggregate(
                        sum_of_jha_qty=Sum('jha_qty'),
                        sum_of_ccc_qty=Sum('ccc_qty'),
                        sum_of_take5_qty=Sum('take5_qty'),
                        sum_of_stop_seek_qty=Sum('stop_seek_qty'),
                        sum_of_mobilised_qty=Sum('mobilised_qty'),
                        sum_of_non_manual_qty=Sum('non_manual_qty'),
                        sum_of_manual_qty=Sum('manual_qty'),
                        sum_of_subcontractor_qty=Sum('subcontractor_qty'),
                        sum_of_environmental_incident_qty=Sum('environmental_incident_qty'),
                        sum_of_near_miss_qty=Sum('near_miss_qty'),
                        sum_of_first_aid_qty=Sum('first_aid_qty'),
                        sum_of_medically_treated_injury_qty=Sum('medically_treated_injury_qty'),
                        sum_of_loss_time_injury_qty=Sum('loss_time_injury_qty')
                    )
                    aggregates = {key: value or 0 for key, value in aggregates.items()}

                    cost_trackings = CostTracking.objects.filter(project_no=project_no, year_week=year_week)
                    cost_aggregates = cost_trackings.aggregate(
                        total_hours_employee=Sum('total_hours_employee'),
                        total_hours_employee_local=Sum('total_hours_employee_local'),
                        total_hours_employee_indigenous=Sum('total_hours_employee_indigenous'),
                        total_amount_employee=Sum('total_amount_employee'),
                        total_hours_equipment=Sum('total_hours_equipment'),
                        total_amount_equipment=Sum('total_amount_equipment')
                    )
                    cost_aggregates = {key: value or 0 for key, value in cost_aggregates.items()}

                    # Calculate percentages
                    total_hours_employee = cost_aggregates['total_hours_employee']
                    total_hours_employee_local = cost_aggregates['total_hours_employee_local']
                    total_hours_employee_indigenous = cost_aggregates['total_hours_employee_indigenous']

                    percentage_employee_local = (total_hours_employee_local / total_hours_employee * 100) if total_hours_employee > 0 else 0
                    percentage_employee_indigenous = (total_hours_employee_indigenous / total_hours_employee * 100) if total_hours_employee > 0 else 0

                    # Combine both aggregate dictionaries
                    aggregates.update(cost_aggregates)
                    aggregates['percentage_employee_local'] = percentage_employee_local
                    aggregates['percentage_employee_indigenous'] = percentage_employee_indigenous

                    # Create or update WeeklyReportList record
                    WeeklyReportList.objects.update_or_create(
                        project_no=project_instance,
                        year_week=year_week,
                        defaults=aggregates
                    )
                    messages.success(request, "Weekly Report created or updated successfully.")
                else:
                    messages.error(request, "No completed daily records exist for the given project and week.")



        return redirect('all_weekly_report')

    context = {
        'unique_projects': sorted(unique_projects, key=lambda x: x[1]),
        'unique_weeks': unique_weeks,
        'new_reports_page': new_reports_page,
    }

    return render(request, 'weekly_report/all_weekly_report.html', context)

@superuser_or_supervisor_required
def view_weekly_report(request, report_id):
    if request.method == 'POST':
        if 'delete_report' in request.POST:
            report_id_to_delete = request.POST.get('delete_report')
            report_to_delete = get_object_or_404(WeeklyReportList, pk=report_id_to_delete)
            report_to_delete.delete()
            messages.success(request, "Weekly Report deleted successfully.")
            return redirect('all_weekly_report')

    report = get_object_or_404(WeeklyReportList, pk=report_id)
    week_number = int(report.year_week[-2:])

    # Generate week numbers for last week and the last three weeks
    previous_week_number = f"{report.year_week[:4]}{str(week_number - 1).zfill(2)}"
    past_week_numbers = [f"{report.year_week[:4]}{str(week_number - i).zfill(2)}" for i in range(1, 4)]

    # Fetch the report for the previous week
    try:
        previous_report = WeeklyReportList.objects.get(year_week=previous_week_number, project_no=report.project_no)
    except WeeklyReportList.DoesNotExist:
        previous_report = None  # If there is no report for the previous week

    # Fetch reports from the last three weeks excluding the current week
    past_reports = WeeklyReportList.objects.filter(
        year_week__in=past_week_numbers,
        project_no=report.project_no
    ).order_by('year_week')[:3]  # Get the last three entries only

    context = {
        'report': report,
        'previous_report': previous_report,
        'past_reports': past_reports
    }
    return render(request, 'weekly_report/view_weekly_report.html', context)