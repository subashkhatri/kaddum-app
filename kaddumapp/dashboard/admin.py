from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group

admin.site.site_header = 'Kaddum App Dashboard'

class DairyRecordAdmin(admin.ModelAdmin):
  list_display = ('project_no', 'record_date', 'record_shift','supervisor','is_draft')

class DayTrackingAdmin(admin.ModelAdmin):
  list_display = ( 'project_no', 'record_date', 'record_shift','kaddum_name','is_draft')

class ShowAllAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        fields = self.model._meta.fields # Get the fields of the model
        field_names = [field.name for field in fields] # Extract the names of the fields
        return field_names # Return the list of field names
    
admin.site.register(DairyRecord, DairyRecordAdmin)
admin.site.register(Project, ShowAllAdmin)
admin.site.register(ResourceCost, ShowAllAdmin)
admin.site.register(DayTracking, DayTrackingAdmin)
admin.site.register(DayTrackingEmployeeDetails, ShowAllAdmin)
admin.site.register(DayTrackingResourceDetails, ShowAllAdmin)


