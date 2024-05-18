from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import DairyRecord, Project, CostTracking, WeeklyReportList



def all_weekly_report(request):
    new_reports = WeeklyReportList.objects.all().order_by('-created_date')
    projects = Project.objects.all()
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

            if CostTracking.objects.filter(project_no=project_no, year_week=year_week).exists():
                dairy_records = DairyRecord.objects.filter(project_no=project_no, year_week=year_week)
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

                cost_trackings = CostTracking.objects.filter(project_no=project_no, year_week=year_week)
                cost_aggregates = cost_trackings.aggregate(
                    sum_of_total_hours_employee = Sum('total_hours_employee'),
                    sum_of_total_hours_employee_local = Sum('total_hours_employee_local'),
                    sum_of_total_hours_employee_indigenous = Sum('total_hours_employee_indigenous'),
                    sum_of_total_amount_employee = Sum('total_amount_employee'),
                    sum_of_total_hours_equipment = Sum('total_hours_equipment'),
                    sum_of_total_amount_equipment = Sum('total_amount_equipment')
                )

                # Create or update WeeklyReportList
                WeeklyReportList.objects.update_or_create(
                    project_no=project_instance,
                    year_week=year_week,
                    defaults={**aggregates}
                )
                messages.success(request, "Weekly Report created successfully.")
            else:
                messages.error(request, "No data found for the given project and week.")


        elif 'delete_report' in request.POST:
            report_id = request.POST.get('delete_report')
            report = get_object_or_404(WeeklyReportList, pk=report_id)
            report.delete()
            messages.success(request, "Weekly Report deleted successfully.")

        return redirect('all_weekly_report')

    context = {
        'unique_projects': sorted(unique_projects, key=lambda x: x[1]),
        'unique_weeks': unique_weeks,
        'new_reports_page': new_reports_page,
    }
    return render(request, 'weekly_report/all_weekly_report.html', context)


def view_weekly_report(request, report_id):
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
        year_week__in=past_week_numbers
    ).order_by('-year_week')[:3]  # Get the last three entries only

    context = {
        'report': report,
        'previous_report': previous_report,
        'past_reports': past_reports
    }
    return render(request, 'weekly_report/view_weekly_report.html', context)
