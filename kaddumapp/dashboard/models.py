from django.db import models

class DairyRecord(models.Model):
    diary_record_id = models.CharField(max_length=10, primary_key=True)
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
