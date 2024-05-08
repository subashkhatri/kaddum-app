from django.shortcuts import render

def all_weekly_report(request):
    context = {}
    return render(request, 'weekly_report/all_weekly_report.html', context)

def view_weekly_report(request):
    context = {}
    return render(request, 'weekly_report/view_weekly_report.html', context)