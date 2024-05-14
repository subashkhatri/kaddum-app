from django.shortcuts import render
from .models import DairyRecord


def index(request):
  dairy_records = DairyRecord.objects.order_by('-created_date')[:10]
  return render(request, 'dashboard/index.html', {'records': dairy_records})

def sample_daily_costing(request):
  return render(request, 'sample_daily_costing.html')