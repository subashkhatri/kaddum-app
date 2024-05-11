from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse 
from .models import DairyRecord, Project, CostTracking, WeeklyReportList, WeeklyStatisticsView
from django.db import connection

def all_weekly_report(request):
    reports = WeeklyStatisticsView.objects.all()
    new_reports = WeeklyReportList.objects.all().order_by('-created_date')
    unique_projects = {(report.project_no, report.project_name) for report in reports}
    unique_weeks = sorted({report.year_week for report in reports})
    
    if request.method == 'POST':
        if 'create_report' in request.POST:
            project_no = request.POST.get('project')
            year_week = request.POST.get('year_week')

            print(f"Searching for Project No: {project_no}, Year Week: {year_week}")
            if WeeklyStatisticsView.objects.filter(project_no=project_no, year_week=year_week).exists():
                project = Project.objects.get(project_no=project_no)
                WeeklyReportList.objects.create(project_no=project, year_week=year_week)
                messages.success(request, "Weekly Report created successfully.")
            else:
                messages.error(request, "No matching data found for the given project and week.")

        elif 'delete_report' in request.POST:
            report_id = request.POST.get('delete_report')
            report = get_object_or_404(WeeklyReportList, pk=report_id)
            report.delete()
            messages.success(request, "Weekly Report deleted successfully.")

        return redirect('all_weekly_report')
    
    context = {
    'reports': reports,
    'unique_projects': sorted(unique_projects, key=lambda x: x[1]),  # Sort by project name
    'unique_weeks': sorted(unique_weeks),
    'new_reports': new_reports
    }        
    return render(request, 'weekly_report/all_weekly_report.html', context)


def view_weekly_report(request):
    report = get_object_or_404(WeeklyReportList, pk=id)
    context = {'report': report}
    return render(request, 'weekly_report/view_weekly_report.html', context)

def delete_weekly_report(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(WeeklyReportList, pk=report_id)
        report.delete()
        messages.success(request, "Weekly report deleted successfully.")
        return redirect('all_weekly_report')
    return redirect('all_weekly_report')