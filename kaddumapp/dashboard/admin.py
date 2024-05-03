from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group

admin.site.site_header = 'Kaddum App Dashboard'

class DairyRecordAdmin(admin.ModelAdmin):
  list_display = ('dairy_record_id', 'project_no', 'record_date', 'record_shift','supervisor_id','created_date','last_modification_date','is_draft')

class DayTrackingAdmin(admin.ModelAdmin):
  list_display = ( 'day_tracking_id','project_no', 'record_date', 'record_shift','created_date','last_modification_date','kaddum_name','is_draft')

class ShowAllAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        fields = self.model._meta.fields # Get the fields of the model
        field_names = [field.name for field in fields] # Extract the names of the fields
        return field_names # Return the list of field names
    

admin.site.register(Project, ShowAllAdmin)
admin.site.register(ResourceCost, ShowAllAdmin)
admin.site.register(DairyRecord, DairyRecordAdmin)
admin.site.register(DayTracking, DayTrackingAdmin)
admin.site.register(DayTrackingEmployeeDetails, ShowAllAdmin)
admin.site.register(DayTrackingEquipmentDetails, ShowAllAdmin)
admin.site.register(CostTracking, ShowAllAdmin)



