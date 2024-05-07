from django.db import models
from django.db.models import Sum, Case, When, F
from users.models import UserAccount
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models_resource_cost import ResourceCost
import os


class Project(models.Model):
    project_no = models.AutoField(primary_key= True)
    purchase_order_no = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=255)
    client = models.CharField(max_length=100)
    project_start_date = models.DateField()
    project_end_date = models.DateField(null=True, blank=True)
    project_budget = models.FloatField(null=True, blank=True)
    project_total_cost = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
        
    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-Project'

    def __str__(self):
        return f"Project No: {self.project_no}, project Name: {self.project_name}"

class DairyRecord(models.Model):
    dairy_record_id = models.CharField(max_length=10, primary_key= True)
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no') # FK from project table
    record_date = models.DateField()
    record_shift = models.CharField(max_length=30)  # value = Day shift or Night shift
    supervisor_id = models.ForeignKey(UserAccount, on_delete=models.PROTECT, db_column ='supervisor_id')  # FK supervisor_id = Useraccount.username
    activity_discussion = models.TextField(null=True, blank=True)
    safety_issue_discussion = models.TextField(null=True, blank=True)
    instruction_from_client = models.TextField(null=True, blank=True)
    visitor_on_site = models.TextField(null=True, blank=True)
    daily_progress_description = models.TextField(null=True, blank=True)
    record_comment = models.TextField(null=True, blank=True)
    handover_note = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)

    #numeric fields
    delay_access = models.BooleanField(default=False)
    delay_lack_of_drawing = models.BooleanField(default=False)
    delay_await_client_decision = models.BooleanField(default=False)
    delay_poor_weather = models.BooleanField(default=False)
    delay_industrial_matters = models.BooleanField(default=False)
    delay_await_client_instruction = models.BooleanField(default=False)
    delay_subcontractors = models.BooleanField(default=False)
    delay_await_materials = models.BooleanField(default=False)
    delay_rework = models.BooleanField(default=False)
    delay_other = models.CharField(max_length=255, null=True, blank=True)
    delay_details = models.TextField(null=True, blank=True)
    
    jha_qty = models.IntegerField(default=0)
    ccc_qty = models.IntegerField(default=0)
    take5_qty = models.IntegerField(default=0)
    stop_seek_qty = models.IntegerField(default=0)
    mobilised_qty = models.IntegerField(default=0)
    non_manual_qty = models.IntegerField(default=0)
    manual_qty = models.IntegerField(default=0)
    subcontractor_qty = models.IntegerField(default=0)
    incident_qty = models.IntegerField(default=0)
    near_miss_qty = models.IntegerField(default=0)
    first_aid_qty = models.IntegerField(default=0)
    medically_treated_injury_qty = models.IntegerField(default=0)
    loss_time_injury_qty = models.IntegerField(default=0)
    
    # draft save
    is_draft = models.BooleanField(default=True)

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DairyRecord'

    def save(self, *args, **kwargs):

        # set dairy_record_id as DR00001, DR0002...
        if not self.dairy_record_id:
            last_record = DairyRecord.objects.all().order_by('-dairy_record_id').first()
            if last_record:
                last_id = int(last_record.dairy_record_id[2:])  # Extract numeric part of ID
                new_id = f"DR{last_id + 1:05}"  # Increment ID
            else:
                new_id = "DR00001"  # If no records exist, start from 1
            self.dairy_record_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Daily Record: {self.dairy_record_id }, Project No: {self.project_no}, Date: {self.record_date}"


class CostTracking(models.Model):
    cost_tracking_id = models.CharField(max_length=10, primary_key=True)  
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no')   #generated automatically
    record_date = models.DateField()                                    #generated automatically   
    year_week = models.CharField(max_length=6, null= True, blank=True)  #generated automatically

    # the below needs to be update when completing costracking
    total_hours = models.FloatField(null= True, blank=True)
    total_hours_local = models.FloatField(null= True, blank=True)
    total_hours_indigenous = models.FloatField(null= True, blank=True)
    total_amount = models.FloatField(null= True, blank=True)
    percentage_hours_indigenous = models.FloatField(null= True, blank=True)
    percentage_hours_local = models.FloatField(null= True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)  
    last_modification_date = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('project_no', 'record_date',)
        app_label = 'dashboard'
        db_table = 'dashboard-CostTracking'

    def save(self, *args, **kwargs):

        # set cost_tracking_id as CT00001, CT00002...
        if not self.cost_tracking_id:
            last_record = CostTracking.objects.all().order_by('-cost_tracking_id').first()
            if last_record:
                last_id = int(last_record.cost_tracking_id[2:])  # Extract numeric part of ID
                new_id = f"CT{last_id + 1:05}"  # Increment ID
            else:
                new_id = "CT00001"  # If no records exist, start from 1
            self.cost_tracking_id = new_id

        # get year_week data like 202417
        if not self.year_week and self.record_date:
            year, week, _ = self.record_date.isocalendar()  # Get ISO year and week
            self.year_week = f"{year}{week:02d}"  # Combine year and week, zero-padded

        # Calculate percentage_hours_local, percentage_hours_indigenous
        if any([
            self.total_hours is not None,
            self.total_hours_indigenous is not None,
            self.total_hours_local is not None,            
        ]):
            total_hours = self.total_hours
            total_hours_local = self.total_hours_local
            total_hours_indigenous = self.total_hours_indigenous

            if total_hours > 0:
                self.percentage_hours_local = (total_hours_local / total_hours) * 100
                self.percentage_hours_indigenous = (total_hours_indigenous / total_hours) * 100
            else:
                self.percentage_hours_local = 0
                self.percentage_hours_indigenous = 0
                
        super().save(*args, **kwargs)


    def __str__(self):
        return f"CostTracking Details: {self.cost_tracking_id}"

class DayTracking(models.Model):
    day_tracking_id = models.CharField(max_length=10, primary_key= True)
    cost_tracking_id = models.ForeignKey(CostTracking, on_delete=models.CASCADE, blank=True, null=True, db_column='cost_tracking_id')
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no') 
    record_date = models.DateField()
    record_shift = models.CharField(max_length=30)
    work_area = models.CharField(max_length=255)
    client_representative = models.CharField(max_length=100)
    weather = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    kaddum_name = models.CharField(max_length=100, blank=True, null=True)
    kaddum_sign = models.ImageField(upload_to='kaddum_signs/', blank=True, null=True)
    kaddum_sign_date = models.DateField(blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_sign = models.ImageField(upload_to='client_signs/', blank=True, null=True)
    client_sign_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingSheet'
    
    def save(self, *args, **kwargs):

        # Set day_tracking_id numbering logic: DS00001, DS00002
        if not self.day_tracking_id:
            last_record = DayTracking.objects.all().order_by('-day_tracking_id').first()
            if last_record:
                last_id = int(last_record.day_tracking_id[2:])  # Extract numeric part of ID
                new_id = f"DS{last_id + 1:05}"  # Increment ID
            else:
                new_id = "DS00001"  # If no records exist, start from 1
            self.day_tracking_id = new_id

        super().save(*args, **kwargs)

        if not self.is_draft:
            # Get or create the assiciated CostTracking record
            cost_tracking, created = CostTracking.objects.get_or_create(
                project_no=self.project_no, 
                record_date=self.record_date, 
                defaults={'total_hours':0}
            )
            
            self.cost_tracking_id = cost_tracking # Assign the CostTracking record to DayTracking

            # Aggregate total hours from related DayTrackingEmployeeDetails
            total_hours = DayTrackingEmployeeDetails.objects.filter(
                day_tracking_id=self.id
            ).aggregate(Sum('total_hours'))['total_hours__sum'] or 0

            # Update the total hours in CostTracking
            cost_tracking.total_hours += total_hours
            cost_tracking.save()

        # It's good practice to call super().save() again if changes are made after the first save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Day Tracking:{self.day_tracking_id} {self.project_no} {self.record_date}"



class DayTrackingEmployeeDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.PROTECT, db_column='day_tracking_id')
    employee_id = models.ForeignKey(UserAccount, on_delete=models.PROTECT, db_column='employee_id')
    position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, related_name='daytracking_employee_details_position', db_column='position_id')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(null= True, blank=True)
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet
    hour_rate = models.FloatField(null= True, blank=True)
    total_amount = models.FloatField(null= True, blank=True)
    confirmed_position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, null=True, blank=True, related_name='daytracking_employee_details_confirmed_position', db_column='confirmed_position_id')

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingEmployeeDetails'

    def save(self, *args, **kwargs):

        if not self.id:
            # get initial position rate
            if self.position_id:
                self.hour_rate = self.position_id.item_rate
        
        if self.total_hours is not None and self.hour_rate is not None:
            # calculate total amount
            self.total_amount = self.total_hours * self.hour_rate

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Day Tracking Employee Details: {self.day_tracking_no}"
    
class DayTrackingEquipmentDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.PROTECT, db_column='day_tracking_id')
    resource_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, db_column='resource_id')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet
    item_rate = models.FloatField(null= True, blank=True)
    total_amount = models.FloatField(null= True, blank=True)
    


    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingEquipmentDetails'

    def save(self, *args, **kwargs):
        # 1. Set default value to item_rate if it's not provided
        if not self.id:
            if self.resource_id:
                self.item_rate = self.resource_id.item_rate
        
        # 2. Calculate the total amount if total_hours and item_rate are provided
        if self.total_hours is not None and self.item_rate is not None:
            self.total_amount = self.total_hours * self.item_rate
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Day Tracking Resource Details: {self.day_tracking_no}"
