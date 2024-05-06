from django.shortcuts import render
from .models import DairyRecord


def index(request):
  dairy_records = DairyRecord.objects.order_by('-created_date')
  return render(request, 'dashboard/index.html', {'records': dairy_records})

