from django.contrib import admin
from .models import DairyRecord
# from django.contrib.auth.models import Group

admin.site.site_header = 'Kaddum App Dashboard'

class DairyRecordAdmin(admin.ModelAdmin):
  list_display = ('job_name', 'client', 'supervisor')

admin.site.register(DairyRecord, DairyRecordAdmin)

