from django.shortcuts import render, redirect
from .models import DairyRecord
from django.contrib.auth.decorators import login_required
from users.decorators import superuser_required, superuser_or_supervisor_required

@login_required(login_url='login')
@superuser_or_supervisor_required
def index(request):
  dairy_records = DairyRecord.objects.order_by('-created_date')[:10]
  return render(request, 'dashboard/index.html', {'records': dairy_records})

def not_found(request, exception):
   return redirect('index')