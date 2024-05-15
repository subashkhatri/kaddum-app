from django.shortcuts import render
from .models import DairyRecord
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
  dairy_records = DairyRecord.objects.order_by('-created_date')[:10]
  return render(request, 'dashboard/index.html', {'records': dairy_records})

