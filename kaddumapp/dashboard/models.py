from django.db import models

class DairyRecord(models.Model):
    job_name = models.CharField(max_length=255, null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    supervisor = models.CharField(max_length=255, null=True, blank=True)
    record_date = models.DateField()
    record_shift = models.CharField(max_length=10)
    activity_discussion = models.TextField(null=True, blank=True)
    safety_issue_discussion = models.TextField(null=True, blank=True)
    instruction_from_client = models.TextField(null=True, blank=True)
    visitor_on_site = models.TextField(null=True, blank=True)
    daily_progress_description = models.TextField(null=True, blank=True)
    record_comment = models.TextField(null=True, blank=True)
    handover_note = models.TextField(null=True, blank=True)
    record_created_date = models.DateField(auto_now_add=True)
    record_submitted_date = models.DateField(null=True, blank=True, auto_now=True)

    # New numeric fields
    mobilised = models.IntegerField(null=True, blank=True)
    non_manual = models.IntegerField(null=True, blank=True)
    manual = models.IntegerField(null=True, blank=True)
    subcontractor = models.IntegerField(null=True, blank=True)
    environmental_incidents = models.IntegerField(null=True, blank=True)
    near_misses = models.IntegerField(null=True, blank=True)
    first_aid = models.IntegerField(null=True, blank=True)
    medically_treated_injury = models.IntegerField(null=True, blank=True)
    loss_time_injury = models.IntegerField(null=True, blank=True)
    # draft save
    is_draft = models.BooleanField(default=True)
    class Meta:
        app_label = 'dashboard'

