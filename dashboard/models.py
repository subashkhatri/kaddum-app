from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum
from users.models import UserAccount
from .models_resource_cost import ResourceCost
from datetime import datetime, timedelta
from datetime import datetime, timedelta



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
        return f"{self.project_no} - {self.project_name}"

class DairyRecord(models.Model):
    dairy_record_id = models.CharField(max_length=10, primary_key= True)
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no') # FK from project table
    record_date = models.DateField()
    year_week = models.CharField(max_length=6, null= True, blank=True)
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
    environmental_incident_qty = models.IntegerField(default=0)
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

        # get year_week data like 202417
        if not self.year_week and self.record_date:
            year, week, _ = self.record_date.isocalendar()  # Get ISO year and week
            self.year_week = f"{year}{week:02d}"  # Combine year and week, zero-padded

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Daily Record: {self.dairy_record_id }, Project No: {self.project_no}, Date: {self.record_date}"


class CostTracking(models.Model):
    cost_tracking_id = models.CharField(max_length=10, primary_key=True)  
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no')   #generated automatically
    record_date = models.DateField()                                    #generated automatically   
    year_week = models.CharField(max_length=6, null= True, blank=True)  #generated automatically

    created_date = models.DateTimeField(auto_now_add=True)  
    last_modification_date = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)

    # the below needs to be update when completing costracking
    total_hours_employee = models.FloatField(default=0)
    total_hours_employee_local = models.FloatField(default=0)
    total_hours_employee_local_percentage = models.FloatField(default=0)
    total_hours_employee_indigenous= models.FloatField(default=0)
    total_hours_employee_indigenous_percentage = models.FloatField(default=0)
    total_amount_employee = models.FloatField(null=True, blank= True)
    total_hours_equipment = models.FloatField(default=0)
    total_amount_equipment = models.FloatField(default=0)
    
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
    cost_tracking_id = models.ForeignKey(CostTracking, on_delete=models.CASCADE, blank=True, null=True, db_column='cost_tracking_id')
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT, db_column='project_no') 
    record_date = models.DateField()
    year_week = models.CharField(max_length=6, null= True, blank=True)  #generated automatically
    record_shift = models.CharField(max_length=30)
    work_area = models.CharField(max_length=255)
    client_representative = models.CharField(max_length=100)
    weather = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    kaddum_name = models.CharField(max_length=100,null=True, blank=True)
    kaddum_sign = models.CharField(max_length=100,null=True, blank=True)
    kaddum_sign_date = models.DateField(null=True, blank=True)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_sign = models.CharField(max_length=100, null=True, blank=True )
    client_sign_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)

    total_hours_employee = models.FloatField(default=0)
    total_hours_employee_local = models.FloatField(default=0)
    total_hours_employee_indigenous= models.FloatField(default=0)
    total_amount_employee = models.FloatField(null=True, blank= True)
    total_hours_equipment = models.FloatField(default=0)
    total_amount_equipment = models.FloatField(default=0)
    
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

        # get year_week data like 202417
        if not self.year_week and self.record_date:
            year, week, _ = self.record_date.isocalendar()  # Get ISO year and week
            self.year_week = f"{year}{week:02d}"  # Combine year and week, zero-padded

        # If DayTracking is completed, create a cost_tracking_instance with project no and create_date
        if not self.is_draft and not self.cost_tracking_id:
            cost_tracking = CostTracking.objects.filter(project_no=self.project_no, record_date=self.record_date).first()

            if cost_tracking:
                self.cost_tracking_id = cost_tracking
            else:
                cost_tracking = CostTracking.objects.create(project_no=self.project_no, record_date=self.record_date)
                self.cost_tracking_id = cost_tracking
        super().save(*args, **kwargs)

        cost_tracking_instance = self.cost_tracking_id
        if cost_tracking_instance:
            day_tracking_aggregates = DayTracking.objects.filter(cost_tracking_id=self.cost_tracking_id).aggregate(
                total_hours_employee=Sum('total_hours_employee'),
                total_hours_employee_local=Sum('total_hours_employee_local'),
                total_hours_employee_indigenous=Sum('total_hours_employee_indigenous'),
                total_amount_employee=Sum('total_amount_employee'),
                total_hours_equipment=Sum('total_hours_equipment'),
                total_amount_equipment=Sum('total_amount_equipment')
            )

            total_hours_employee = day_tracking_aggregates['total_hours_employee'] or 0
            total_hours_employee_local = day_tracking_aggregates['total_hours_employee_local'] or 0
            total_hours_employee_indigenous = day_tracking_aggregates['total_hours_employee_indigenous'] or 0
            total_amount_employee = day_tracking_aggregates['total_amount_employee'] or 0
            total_hours_equipment = day_tracking_aggregates['total_hours_equipment'] or 0
            total_amount_equipment = day_tracking_aggregates['total_amount_equipment'] or 0

            local_percentage = 0 if total_hours_employee == 0 else (total_hours_employee_local / total_hours_employee)*100
            indigenous_percentage = 0 if total_hours_employee == 0 else (total_hours_employee_indigenous / total_hours_employee)*100

            # Update corresponding CostTracking instance
            cost_tracking_instance.total_hours_employee = total_hours_employee
            cost_tracking_instance.total_hours_employee_local = total_hours_employee_local
            cost_tracking_instance.total_hours_employee_indigenous = total_hours_employee_indigenous
            cost_tracking_instance.total_amount_employee = total_amount_employee
            cost_tracking_instance.total_hours_equipment = total_hours_equipment
            cost_tracking_instance.total_amount_equipment = total_amount_equipment
            cost_tracking_instance.total_hours_employee_local_percentage = local_percentage
            cost_tracking_instance.total_hours_employee_indigenous_percentage = indigenous_percentage

            cost_tracking_instance.save()


    def __str__(self):
        return f"Day Tracking:{self.day_tracking_id} {self.record_date}"


class DayTrackingEmployeeDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.CASCADE, db_column='day_tracking_id')
    employee_id = models.ForeignKey(UserAccount, on_delete=models.PROTECT, db_column='employee_id')
    position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, related_name='daytracking_employee_details_position', db_column='position_id')
    start_time = models.TimeField()
    end_time = models.TimeField()
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet, and will automatically fetch from other table
    hour_rate = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    confirmed_position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, null=True, blank=True, related_name='daytracking_employee_details_confirmed_position', db_column='confirmed_position_id')

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingEmployeeDetails'

    def save(self, *args, **kwargs):
        if not self.id:
            last_record = DayTrackingEmployeeDetails.objects.all().order_by('-id').first()
            if last_record:
                last_id = int(last_record.id)  # Extract numeric part of ID
                new_id = last_id + 1  # Increment ID
            else:
                new_id = 1  # If no records exist, start from 1
            self.id = new_id
        
        # Calculate total hours
        if isinstance(self.start_time, str):
            self.start_time = datetime.strptime(self.start_time, '%H:%M').time() 
        if isinstance(self.end_time, str):
            self.end_time = datetime.strptime(self.end_time, '%H:%M').time()
        start_time_obj = self.start_time
        end_time_obj = self.end_time
        if start_time_obj and end_time_obj:
            start_time_seconds = (start_time_obj.hour * 3600) + (start_time_obj.minute * 60) + start_time_obj.second
            end_time_seconds = (end_time_obj.hour * 3600) + (end_time_obj.minute * 60) + end_time_obj.second
            total_seconds = end_time_seconds - start_time_seconds
            self.total_hours = abs(total_seconds / 3600)  # Convert seconds to hours
        
        if self.position_id:
            self.hour_rate = self.position_id.item_rate

        # Calculate total amount
        if self.total_hours is not None and self.hour_rate is not None:
            self.total_amount = float(self.total_hours) * float(self.hour_rate)

        super().save(*args, **kwargs)

        # Update total hours for the related DayTracking instance
        day_tracking_instance = self.day_tracking_id
        if day_tracking_instance:
            total_hours_employee = DayTrackingEmployeeDetails.objects.filter(day_tracking_id=self.day_tracking_id).aggregate(total_hours_employee=Sum('total_hours'))['total_hours_employee'] or 0
            total_hours_employee_local = DayTrackingEmployeeDetails.objects.filter(day_tracking_id=self.day_tracking_id, employee_id__is_local=True).aggregate(total_hours_employee_local=Sum('total_hours'))['total_hours_employee_local'] or 0
            total_hours_employee_indigenous = DayTrackingEmployeeDetails.objects.filter(day_tracking_id=self.day_tracking_id, employee_id__is_indigenous=True).aggregate(total_hours_employee_indigenous=Sum('total_hours'))['total_hours_employee_indigenous'] or 0
            total_amount_employee = DayTrackingEmployeeDetails.objects.filter(day_tracking_id=self.day_tracking_id).aggregate(total_amount_employee=Sum('total_amount'))['total_amount_employee'] or 0

            # Update the DayTracking instance fields
            day_tracking_instance.total_hours_employee = total_hours_employee
            day_tracking_instance.total_hours_employee_local = total_hours_employee_local
            day_tracking_instance.total_hours_employee_indigenous = total_hours_employee_indigenous
            day_tracking_instance.total_amount_employee = total_amount_employee
            day_tracking_instance.save()


    def __str__(self):
        return f"{self.id}: {self.day_tracking_id}"
    
class DayTrackingEquipmentDetails(models.Model):
    id = models.AutoField(primary_key= True)
    day_tracking_id = models.ForeignKey(DayTracking, on_delete=models.CASCADE, db_column='day_tracking_id')
    resource_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, db_column='resource_id')
    start_time = models.TimeField()
    end_time = models.TimeField()
    work_description = models.CharField(max_length=255, null=True, blank=True)

    # the below is for cost tracking sheet,and will automatically fetch from other table
    item_rate = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-DayTrackingEquipmentDetails'

    def save(self, *args, **kwargs):
        if not self.id:
            last_record = DayTrackingEmployeeDetails.objects.all().order_by('-id').first()
            if last_record:
                last_id = int(last_record.id)  # Extract numeric part of ID
                new_id = last_id+1  # Increment ID
            else:
                new_id = "1"  # If no records exist, start from 1
            self.id = new_id

         # calculate start_time and end_time to total hours
        if isinstance(self.start_time, str):
            self.start_time = datetime.strptime(self.start_time, '%H:%M').time()
        if isinstance(self.end_time, str):
            self.end_time = datetime.strptime(self.end_time, '%H:%M').time()       
        start_time_obj = self.start_time
        end_time_obj = self.end_time
        if start_time_obj and end_time_obj:
            start_time_seconds = (start_time_obj.hour * 3600) + (start_time_obj.minute * 60) + start_time_obj.second
            end_time_seconds = (end_time_obj.hour * 3600) + (end_time_obj.minute * 60) + end_time_obj.second
            total_seconds = end_time_seconds - start_time_seconds
            self.total_hours = abs(total_seconds / 3600)  # Convert seconds to hours

        if self.resource_id:
            self.item_rate = self.resource_id.item_rate

        super().save(*args, **kwargs)
        day_tracking_instance = self.day_tracking_id
        if day_tracking_instance:
            total_hours_equipment = DayTrackingEquipmentDetails.objects.filter(day_tracking_id=self.day_tracking_id).aggregate(total_hours_equipment=Sum('total_hours'))['total_hours_equipment'] or 0
            total_amount_equipment = DayTrackingEquipmentDetails.objects.filter(day_tracking_id=self.day_tracking_id).aggregate(total_amount_equipment=Sum('item_rate'))['total_amount_equipment'] or 0

            # Update the DayTracking instance fields
            day_tracking_instance.total_hours_equipment = total_hours_equipment
            day_tracking_instance.total_amount_equipment = total_amount_equipment
            day_tracking_instance.save()        

        
    def __str__(self):
        return f"{self.id}: {self.day_tracking_id}"
   
    
class WeeklyReportList(models.Model):
    report_id = models.AutoField(primary_key=True)
    project_no = models.ForeignKey(Project, on_delete=models.PROTECT,db_column='project_no')
    year_week = models.CharField(max_length=6)
    start_date = models.DateField(null= True, blank=True)
    end_date = models.DateField(null= True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sum_of_jha_qty = models.IntegerField(default=0)
    sum_of_ccc_qty = models.IntegerField(default=0)
    sum_of_take5_qty = models.IntegerField(default=0)
    sum_of_stop_seek_qty = models.IntegerField(default=0)
    sum_of_mobilised_qty = models.IntegerField(default=0)
    sum_of_non_manual_qty = models.IntegerField(default=0)
    sum_of_manual_qty = models.IntegerField(default=0)
    sum_of_subcontractor_qty = models.IntegerField(default=0)
    sum_of_environmental_incident_qty = models.IntegerField(default=0)
    sum_of_near_miss_qty = models.IntegerField(default=0)
    sum_of_first_aid_qty = models.IntegerField(default=0)
    sum_of_medically_treated_injury_qty = models.IntegerField(default=0)
    sum_of_loss_time_injury_qty = models.IntegerField(default=0)
    total_hours_employee = models.FloatField(default=0)
    total_hours_employee_local = models.FloatField(default=0)
    total_hours_employee_indigenous= models.FloatField(default=0)
    total_amount_employee = models.FloatField(null=True, blank= True,default=0)
    total_hours_equipment = models.FloatField(default=0)
    total_amount_equipment = models.FloatField(default=0)
    percentage_employee_local = models.FloatField(default=0)
    percentage_employee_indigenous = models.FloatField(default=0)
 
    class Meta:
        app_label = 'dashboard'
        db_table = 'Report-WeeklyReportList'
   
    def save(self, *args, **kwargs):
        if self.year_week:
            # Assuming year_week is in the format 'YYYYWW'
            year = int(self.year_week[:4])
            week = int(self.year_week[4:])
            # Calculate start date based on ISO 8601 week date
            start_date = datetime.strptime(f'{year}-W{week-1}-1', "%Y-W%W-%w").date()
            # Calculate end date by adding 6 days to the start date
            end_date = start_date + timedelta(days=6)
            self.start_date = start_date
            self.end_date = end_date
        super().save(*args, **kwargs)
 
 
