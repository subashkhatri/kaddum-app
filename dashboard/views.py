from django.shortcuts import render, redirect
from .models import DairyRecord, DayTracking
from django.contrib.auth.decorators import login_required
from users.decorators import superuser_required, superuser_or_supervisor_required

@login_required(login_url='login')
@superuser_or_supervisor_required
def index(request):
  dairy_records = DairyRecord.objects.filter(is_draft=True).order_by('-created_date')[:5]
  day_trackings = DayTracking.objects.filter(is_draft=True).order_by('-created_date')[:5]
  return render(request, 'dashboard/index.html', {'dairy_records': dairy_records, 'day_trackings': day_trackings})

def not_found(request, exception):
   return render(request, '404.html')