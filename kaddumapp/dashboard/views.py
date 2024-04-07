from django.shortcuts import render

def index(request):
  return render(request, 'index.html')

def dairy_record(request):
  return render(request, 'dairy_record.html')
