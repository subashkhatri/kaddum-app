from django.contrib import admin
from .models import DairyRecord
from django.contrib.auth.models import Group

admin.site.site_header = 'Kaddum App Dashboard'

admin.site.register(DairyRecord)

