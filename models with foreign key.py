from django.db import models

class EmployeeStatus(models.Model):
    EmployeeStatusCode = models.CharField(max_length=5, primary_key=True)
    EmployeeStatusName = models.CharField(max_length=100)
    StatusDescription = models.TextField()

    def __str__(self):
        return self.EmployeeStatusName

class ProjectStatus(models.Model):
    ProjectStatusCode = models.CharField(max_length=5, primary_key=True)
    ProjectStatusName = models.CharField(max_length=100)
    StatusDescription = models.TextField()

    def __str__(self):
        return self.ProjectStatusName

class FileStatus(models.Model):
    FileStatusCode = models.CharField(max_length=5, primary_key=True)
    FileStatusName = models.CharField(max_length=100)
    StatusDescription = models.TextField()

    def __str__(self):
        return self.FileStatusName

class Employee(models.Model):
    EmployeeId = models.CharField(max_length=10, primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    FullName = models.CharField(max_length=255)
    Indigenous = models.BooleanField()
    Local = models.BooleanField()
    Position = models.CharField(max_length=255)
    EmployeeStatusCode = models.ForeignKey('EmployeeStatus', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"
    
    def save(self, *args, **kwargs):
        # Concatenate first name and last name to create full name
        self.FullName = f"{self.FirstName} {self.LastName}"
        super().save(*args, **kwargs)
    
class Project(models.Model):
    ProjectNo = models.IntegerField(primary_key=True)
    PurchaseOrderNo = models.CharField(max_length=100, null=True, blank=True)
    JobName = models.CharField(max_length=255)
    Client = models.CharField(max_length=100)
    ProjectStartDate = models.DateField()
    ProjectEndDate = models.DateField()
    ProjectBudget = models.FloatField(decimal_places=2)
    ProjectTotalCost = models.FloatField(decimal_places=2)
    ProjectStatusCode = models.ForeignKey('ProjectStatus', on_delete=models.CASCADE)

    def __str__(self):
        return f"Project No: {self.ProjectNo}, Job Name: {self.JobName}"

class DiaryRecord(models.Model):
    DiaryRecordNo = models.CharField(max_length=10, primary_key=True)
    ProjectNo = models.ForeignKey(Project, on_delete=models.CASCADE)
    RecordDate = models.DateField()
    RecordShift = models.CharField(max_length=10)
    SupervisorId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DelayAccess = models.BooleanField(default=False)
    DelayLackOfDrawing = models.BooleanField(default=False)
    DelayAwaitClientDecision = models.BooleanField(default=False)
    DelayPoorWeather = models.BooleanField(default=False)
    DelayIndustrialMatters = models.BooleanField(default=False)
    DelayAwaitClientInstruction = models.BooleanField(default=False)
    DelaySubcontractors = models.BooleanField(default=False)
    DelayAwaitMaterials = models.BooleanField(default=False)
    DelayRework = models.BooleanField(default=False)
    DelayOther = models.CharField(max_length=255, null=True, blank=True)
    DelayDetails = models.TextField(null=True, blank=True)
    ActivityDiscussion = models.TextField(null=True, blank=True)
    SafetyIssueDiscussion = models.TextField(null=True, blank=True)
    InstructionFromClient = models.TextField(null=True, blank=True)
    VisitorOnSite = models.TextField(null=True, blank=True)
    DailyProgressDescription = models.TextField(null=True, blank=True)
    RecordComment = models.TextField(null=True, blank=True)
    HandoverNote = models.TextField(null=True, blank=True)
    JhaQty = models.IntegerField(default=0)
    CccQty = models.IntegerField(default=0)
    Take5Qty = models.IntegerField(default=0)
    StopSeekQty = models.IntegerField(default=0)
    MobilisedQty = models.IntegerField(default=0)
    NonManualQty = models.IntegerField(default=0)
    ManualQty = models.IntegerField(default=0)
    SubcontractorQty = models.IntegerField(default=0)
    IncidentQty = models.IntegerField(default=0)
    NearMissQty = models.IntegerField(default=0)
    FirstAidQty = models.IntegerField(default=0)
    MedicallyTreatedInjuryQty = models.IntegerField(default=0)
    LossTimeInjuryQty = models.IntegerField(default=0)
    RecordCreatedDate = models.DateField()
    RecordSubmittedDate = models.DateField(null=True, blank=True)
    FileStatusCode = models.ForeignKey(FileStatus, on_delete=models.CASCADE)
    def __str__(self):
        return f"Diary Record: {self.DiaryRecordNo}, Project No: {self.ProjectNo}, Date: {self.RecordDate}"

class DayTracking(models.Model):
    DayTrakingNo = models.CharField(max_length=50, primary_key= True)
    ProjectNo = models.ForeignKey(Project, on_delete=models.CASCADE)
    RecordDate = models.DateField()
    Shift = models.CharField(max_length=50)
    WorkArea = models.CharField(max_length=255)
    ClientRepresentative = models.CharField(max_length=100)
    Weather = models.CharField(max_length=100)
    Comments = models.TextField(null=True, blank=True)
    KaddumName = models.CharField(max_length=100, blank=True, null=True)
    KaddumSign = models.ImageField(upload_to='kaddum_signs/', blank=True, null=True)
    KaddumSignDate = models.DateField(blank=True, null=True)
    ClientName = models.CharField(max_length=100, blank=True, null=True)
    ClientSign = models.ImageField(upload_to='client_signs/', blank=True, null=True)
    ClientSignDate = models.DateField(blank=True, null=True)
    SubmittedDate = models.DateField()
    FileStatusCode = models.ForeignKey(FileStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Day Tracking:{self.DayTrakingNo} Project No: {self.ProjectNo}"

class DayTrackingEmployeeDetails(models.Model):
    LineItemNo = models.CharField(max_length=50, primary_key=True)
    DayTrackingNo = models.ForeignKey(DayTracking, on_delete=models.CASCADE)
    EmployeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Role = models.CharField(max_length=100)
    HourRate = models.FloatField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    TotalHours = models.DecimalField(max_digits=10, decimal_places=2)
    WorkDescription = models.CharField(max_length=255)

    def __str__(self):
        return f"Day Tracking:{self.DayTrackingNo} Project No: {self.LineItemNo}"

class DayTrackingEquipDetails(models.Model):
    LineItemNo = models.CharField(max_length=50, primary_key=True)
    DayTrackingNo = models.ForeignKey(DayTracking, on_delete=models.CASCADE)
    CostItemId = models.CharField(max_length=50)
    HourRate = models.FloatField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    TotalHours = models.DecimalField(max_digits=5, decimal_places=2)
    TotalCost = models.DecimalField(max_digits=10, decimal_places=2)
    WorkDescription = models.CharField(max_length=255)

    def __str__(self):
        return f"Day Tracking:{self.DayTrackingNo} Project No: {self.LineItemNo}"

class CostTracking(models.Model):
    LineItemNo = models.IntegerField(primary_key=True)
    ProjectNo = models.ForeignKey(Project, on_delete=models.CASCADE)
    DayTrackingNo = models.ForeignKey(DayTracking, on_delete=models.CASCADE)
    Date = models.DateField()
    Shift = models.CharField(max_length=50)
    YearWeek = models.CharField(max_length=10)
    EmployeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ConfirmRole = models.CharField(max_length=100)
    ConfirmRate = models.FloatField()
    ConfirmStartTime = models.TimeField()
    ConfirmEndTime = models.TimeField()
    ConfirmTotalHour = models.DecimalField(max_digits=5, decimal_places=2)
    ConfirmTotalCost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.LineItemNo)