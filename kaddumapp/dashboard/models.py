from django.db import models

class Project(models.Model):
    project_no = models.AutoField(primary_key= True)
    purchase_order_no = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=255)
    client = models.CharField(max_length=100)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True)
    project_budget = models.FloatField(null=True, blank=True)
    project_total_cost = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
        
    class Meta:
        app_label = 'dashboard'

    def __str__(self):
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
        return f"Resource: {self.resource_item_no}, name: {self.item_name} cost rate: {self.item_rate}"
    

class DairyRecord(models.Model):
    project_no = models.CharField(max_length=5)
    record_date = models.DateField()
    record_shift = models.CharField(max_length=10)
    supervisor = models.CharField(max_length=100)
    activity_discussion = models.TextField(null=True, blank=True)
    safety_issue_discussion = models.TextField(null=True, blank=True)
    instruction_from_client = models.TextField(null=True, blank=True)
    visitor_on_site = models.TextField(null=True, blank=True)
    daily_progress_description = models.TextField(null=True, blank=True)
    record_comment = models.TextField(null=True, blank=True)
    handover_note = models.TextField(null=True, blank=True)
    record_created_date = models.DateField(auto_now_add=True)
    record_submitted_date = models.DateField(null=True, blank=True, auto_now=True)

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

    def __str__(self):
        return f"Daily Record: {self.id}, Project No: {self.project_no}, Date: {self.record_date}"

class DayTracking(models.Model):
    project_no = models.CharField(max_length=5)
    record_date = models.DateField()
    record_day = models.CharField(max_length=10)
    record_shift = models.CharField(max_length=50)
    work_area = models.CharField(max_length=255)
    client_representative = models.CharField(max_length=100)
    weather = models.TextField()
    comments = models.TextField(null=True, blank=True)
    kaddum_name = models.CharField(max_length=100, blank=True, null=True)
    kaddum_sign = models.ImageField(upload_to='kaddum_signs/', blank=True, null=True)
    kaddum_sign_date = models.DateField(blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_sign = models.ImageField(upload_to='client_signs/', blank=True, null=True)
    client_sign_date = models.DateField(blank=True, null=True)
    record_created_date = models.DateField(auto_now_add=True)
    record_submitted_date = models.DateField(null=True, blank=True, auto_now=True)
    is_draft = models.BooleanField(default=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Day Tracking:{self.day_tracking_no} "
    
class DayTrackingEmployeeDetails(models.Model):
    day_tracking_no = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=255)
    position = models.CharField(max_length=50)  # job position
    item_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.FloatField()
    work_description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Day Tracking Employee Details: {self.day_tracking_no}"
    
class DayTrackingResourceDetails(models.Model):
    day_tracking_no = models.CharField(max_length=50)
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.FloatField()
    work_description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f"Day Tracking Resource Details: {self.day_tracking_no}"
    