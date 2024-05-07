from django import forms
from django.forms.models import inlineformset_factory
from .models import DayTracking, DayTrackingEmployeeDetails, DayTrackingEquipmentDetails, Project, ResourceCost, UserAccount

class DayTrackingForm(forms.ModelForm):
    project_no = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label="Project",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is mandatory"}
    )
    client_representative = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    work_area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    weather = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    kaddum_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    kaddum_sign_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    client_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_sign_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

    class Meta:
        model = DayTracking
        fields = [
            'project_no', 'record_date', 'record_shift', 'work_area',
            'client_representative', 'weather', 'comments', 'kaddum_name',
            'kaddum_sign', 'kaddum_sign_date', 'client_name', 'client_sign',
            'client_sign_date'
        ]
        widgets = {
            'record_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'record_shift': forms.Select(choices=[('Dayshift', 'Dayshift'), ('Nightshift', 'Nightshift')], attrs={'class': 'form-control'}),
        }

DayTrackingEmployeeFormset = inlineformset_factory(
    DayTracking,
    DayTrackingEmployeeDetails,
    fields=('employee_id', 'position_id', 'start_time', 'end_time', 'total_hours', 'work_description'),
    extra=1,
    widgets={
        'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        'work_description': forms.TextInput(attrs={'class': 'form-control'})
    }
)

DayTrackingEquipmentFormset = inlineformset_factory(
    DayTracking,
    DayTrackingEquipmentDetails,
    fields=('resource_id', 'start_time', 'end_time', 'total_hours', 'work_description', 'item_rate', 'total_amount'),
    extra=1,
    widgets={
        'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        'work_description': forms.TextInput(attrs={'class': 'form-control'}),
        'item_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        'total_amount': forms.NumberInput(attrs={'class': 'form-control'})
    }
)
