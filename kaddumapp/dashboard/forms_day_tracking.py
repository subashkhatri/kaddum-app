from django import forms
from django.forms.models import inlineformset_factory
from .models import DayTracking, DayTrackingEmployeeDetails, DayTrackingEquipmentDetails, Project, ResourceCost, UserAccount


SHIFT_CHOICES = [
        ('', 'Please select...'),
        ('morning', 'Day Shift'),
        ('evening', 'Night Shift'),
    ]


class DayTrackingForm(forms.ModelForm):
    
    record_shift = forms.ChoiceField(
        label="*Record Shift",
        choices=SHIFT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model= DayTracking
        exclude = ['day_tracking_id', 'year_week', 'created_date', 'last_modification_date','is_draft','total_hours_employee','total_hours_employee_local','total_hours_employee_indigenous','total_amount_employee','total_hours_equipment','total_amount_equipment']
        widgets={
            'Project_no': forms.Select(attrs={'class': 'form-control'}),  
            'record_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'record_shift': forms.TextInput(attrs={'class': 'form-control'}),
            'work_area': forms.TextInput(attrs={'class': 'form-control'}),
            'client_representative': forms.TextInput(attrs={'class': 'form-control'}),
            'weather': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'kaddum_name': forms.TextInput(attrs={'class': 'form-control'}),
            'kaddum_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'kaddum_sign_date': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_sign_date': forms.TextInput(attrs={'class': 'form-control'}), 
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            projects = Project.objects.all().values_list('project_no','project_name')
            self.fields['Project_no'].choices = [('', 'Please select...')] + list(projects)

DayTrackingEmployeeFormSet = inlineformset_factory(
        DayTracking,
        DayTrackingEmployeeDetails,
        fields=('employee_id', 'position_id', 'start_time', 'end_time', 'total_hours', 'work_description'),
        extra=5,
        widgets={
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'work_description': forms.TextInput(attrs={'class': 'form-control'})
        }
    )

DayTrackingEquipmentFormSet = inlineformset_factory(
        DayTracking,
        DayTrackingEquipmentDetails,
        fields=('resource_id', 'start_time', 'end_time', 'total_hours', 'work_description', 'item_rate'),
        extra=5,
        widgets={
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'work_description': forms.TextInput(attrs={'class': 'form-control'}),
            'item_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'total_amount': forms.NumberInput(attrs={'class': 'form-control'})
        }
    )

class DayTrackingCombinedForm(forms.Form):
    day_tracking = DayTrackingForm()
    employee_formset = DayTrackingEmployeeFormSet(prefix='employees', queryset=DayTrackingEmployeeDetails.objects.none())
    equipment_formset = DayTrackingEquipmentFormSet(prefix='equipment', queryset=DayTrackingEquipmentDetails.objects.none())