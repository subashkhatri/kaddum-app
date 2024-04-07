from django.shortcuts import render

def index(request):
  return render(request, 'dashboard/index.html')

def dairy_record(request):
  return render(request, 'dashboard/dairy_record.html')
