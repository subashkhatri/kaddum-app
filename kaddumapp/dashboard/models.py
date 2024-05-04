from django.db import models
from django.db.models import Sum, Case, When, F
from users.models import UserAccount
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
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
<<<<<<< HEAD
        return f"Project No: {self.project_no}, Job Name: {self.project_name}"

class ResourceCost(models.Model):
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_id = models.CharField(max_length=10, null=True, blank=True)
    item_location = models.CharField(max_length=30, null=True, blank=True)
    item_rate = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=10)
    mobilisation_desc = models.CharField(max_length=50, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Resource: {self.id}, name: {self.item_name} cost rate: {self.item_rate}"
    
=======
        return f"Project No: {self.project_no}, project Name: {self.project_name}"
>>>>>>> origin/feature/daily-record-models-add-foreign-key

class DairyRecord(models.Model):
    dairy_record_id = models.CharField(max_length=10, primary_key= True)
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT) # FK from project table
    record_date = models.DateField()
    record_shift = models.CharField(max_length=30)  # value = Day shift or Night shift
    supervisor_id = models.ForeignKey(UserAccount, on_delete=models.PROTECT)  # FK supervisor_id = Useraccount.username
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
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT)   #generated automatically
    record_date = models.DateField()                                    #generated automatically   
    year_week = models.CharField(max_length=6, null= True, blank=True)  #generated automatically

    # the below needs to be update when completing costracking
    total_hours = models.FloatField(null= True, blank=True)
    total_hours_local = models.FloatField(null= True, blank=True)
    total_hours_indigenous = models.FloatField(null= True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

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

        super().save(*args, **kwargs)


    def __str__(self):
        return f"CostTracking Details: {self.cost_tracking_id}"

class DayTracking(models.Model):
    day_tracking_id = models.CharField(max_length=10, primary_key= True)
    cost_tracking_id = models.ForeignKey(CostTracking, on_delete=models.CASCADE, blank=True, null=True)
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT) 
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

        # If DayTracking is completed, create a cost_tracking_instance with project no and create_date
        if not self.is_draft and not self.cost_tracking_id:
            # Check if a CostTracking record exists for the project and record date
            cost_tracking = CostTracking.objects.filter(project_no=self.project_no, record_date=self.record_date).first()

            if cost_tracking:
                self.cost_tracking_id = cost_tracking
            else:
                # Create a new CostTracking record
                cost_tracking = CostTracking.objects.create(project_no=self.project_no, record_date=self.record_date)
                self.cost_tracking_id = cost_tracking

        super().save(*args, **kwargs)


    def __str__(self):
<<<<<<< HEAD
        return f"Day Tracking:{self.id} {self.project_no} {self.record_date}"
    
=======
        return f"Day Tracking:{self.day_tracking_id} {self.project_no} {self.record_date}"



>>>>>>> origin/feature/daily-record-models-add-foreign-key
class DayTrackingEmployeeDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.PROTECT)
    employee_id = models.ForeignKey(UserAccount, on_delete=models.PROTECT)
    position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, related_name='daytracking_employee_details_position')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet
    hour_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    confirmed_position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, null=True, blank=True, related_name='daytracking_employee_details_confirmed_position')

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingEmployeeDetails'

    def save(self, *args, **kwargs):

        if not self.id:
            # get initial position rate
            if self.position_id:
                self.hour_rate = self.position_id.hour_rate
        
        if self.total_hours is not None and self.hour_rate is not None:
            # calculate total amount
            self.total_amount = Decimal(self.total_hours) * self.hour_rate

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Day Tracking Employee Details: {self.day_tracking_no}"
    
class DayTrackingEquipmentDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.PROTECT)
    resource_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet
    item_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    


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
            self.total_amount = Decimal(self.total_hours) * self.item_rate
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Day Tracking Resource Details: {self.day_tracking_no}"
<<<<<<< HEAD

class CostTracking(models.Model):
    project_no = models.CharField(max_length=5)
    record_date = models.DateField()
    record_day = models.CharField(max_length=10)
    year_week = models.CharField(max_length=6, null= True, blank=True)
    total_hours = models.FloatField(null= True, blank=True)
    local_hours = models.FloatField(null= True, blank=True)
    indigenous_hours = models.FloatField(null= True, blank=True)
    total_amount = models.FloatField(null= True, blank=True)
    local_amount = models.FloatField(null= True, blank=True)
    indigenous_amount = models.FloatField(null= True, blank=True)
    record_created_date = models.DateField(auto_now_add=True)
    record_submitted_date = models.DateField(null=True, blank=True, auto_now=True)
    is_draft = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'dashboard'

    def save(self, *args, **kwargs):
        if not self.year_week and self.record_date:
            year, week, _ = self.record_date.isocalendar()  # Get ISO year and week
            self.year_week = f"{year}{week:02d}"  # Combine year and week, zero-padded
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Day Tracking Resource Details: {self.id}"

class CostingEmployeeDetails(models.Model):
    cost_tracking_no = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=255)
    position = models.CharField(max_length=50)  # job position
    item_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Cost Tracking Employee Details: {self.cost_tracking_no}"
    
class CostingResourceDetails(models.Model):
    cost_tracking_no = models.CharField(max_length=50)
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Cost Tracking Resource Details: {self.cost_tracking_no}"
=======
>>>>>>> origin/feature/daily-record-models-add-foreign-key
