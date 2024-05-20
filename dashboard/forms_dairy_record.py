from django import forms

from .models_resource_cost import ResourceCost
from .models import (
    DairyRecord,
    Project,
    CostTracking,
)
from users.models import UserAccount

SHIFT_CHOICES = [
        ('Day Shift', 'Day Shift'),
        ('Night Shift', 'Night Shift'),
    ]
def validate_non_negative(value):
      if value < 0:
          raise forms.ValidationError("The {value} quantity cannot be less than 0.")

class DairyRecordForm(forms.ModelForm):

    project_no = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label="*Project",
        empty_label="Select a Project",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is mandatory"}
    )
    supervisor_id = forms.ModelChoiceField(
        queryset=UserAccount.objects.all(),
        label="*Supervisor",
        empty_label="Select a Supervisor",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is mandatory"},
    )
    record_shift = forms.ChoiceField(
        label= "*Record shift",
        choices=SHIFT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DairyRecord
        exclude = ['dairy_record_id']
        widgets = {
          "record_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
          "activity_discussion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "safety_issue_discussion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "instruction_from_client": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "visitor_on_site": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "daily_progress_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "record_comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "handover_note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "delay_access": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_lack_of_drawing": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_await_client_decision": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_poor_weather": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_industrial_matters": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_await_client_instruction": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_subcontractors": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_await_materials": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_rework": forms.CheckboxInput(attrs={"class": "form-check-input"}),
          "delay_other": forms.TextInput(attrs={"class": "form-control"}),
          "delay_details": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
          "jha_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "ccc_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "take5_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "stop_seek_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "mobilised_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "non_manual_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "manual_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "subcontractor_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "environmental_incident_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "near_miss_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "first_aid_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "medically_treated_injury_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "loss_time_injury_qty": forms.NumberInput(attrs={"class": "form-control"}),
          "is_draft": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            'record_date': '*Record Date',
            'delay_access': 'Access',
            'delay_lack_of_drawing': 'Lack of Drawing',
            'delay_await_client_decision': 'Await client decision',
            'delay_industrial_matters': 'Industrial Matters',
            'delay_await_client_instruction': 'Await client instruction',
            'delay_subcontractors': 'Subcontractors',
            'delay_await_materials': 'Await Materials',
            'delay_rework': 'Re-work',
            'delay_other': 'Other',
        }


    def __init__(self, *args, **kwargs):
        super(DairyRecordForm, self).__init__(*args, **kwargs)
        integer_fields = [
            'jha_qty', 'ccc_qty', 'take5_qty', 'stop_seek_qty', 'mobilised_qty',
            'non_manual_qty', 'manual_qty', 'subcontractor_qty', 'environmental_incident_qty',
            'near_miss_qty', 'first_aid_qty', 'medically_treated_injury_qty', 'loss_time_injury_qty'
        ]

        for field_name in integer_fields:
            self.fields[field_name].validators.append(validate_non_negative)
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

        # Check if there is a CostTracking record for the same project and date that is not a draft
        project_no = cleaned_data.get('project_no')
        record_date = cleaned_data.get('record_date')
        if project_no and record_date:
            cost_tracking_confirmed = CostTracking.objects.filter(
                project_no = project_no,
                record_date = record_date,
                is_draft = False
            ).exists()
            if cost_tracking_confirmed:
                self.add_error('record_date','Please check the record date, as Cost Tracking Record is already confirmed.')
