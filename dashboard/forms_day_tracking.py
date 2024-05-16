from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import (
    DayTracking,
    DayTrackingEmployeeDetails,
    DayTrackingEquipmentDetails,
    Project,
    UserAccount
)
from .models_resource_cost import ResourceCost
from django.core.exceptions import ValidationError

class DayTrackingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    

    record_shift = forms.ChoiceField(
        label="*Record Shift",
        choices=[('', 'Please select...'),('Day Shift', 'Day Shift'),('Night Shift', 'Night Shift')],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    project_no = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label="*Project",
        empty_label="Please select...",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is mandatory"},
        required= True
    )

    class Meta:
        model= DayTracking
        fields = ['project_no','record_date','work_area','client_representative','weather', 'comments', 'kaddum_name','kaddum_sign','kaddum_sign_date','client_name','client_sign','client_sign_date','record_shift']
        widgets={
            'record_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'work_area': forms.TextInput(attrs={'class': 'form-control'}),
            'client_representative': forms.TextInput(attrs={'class': 'form-control'}),
            'weather': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'kaddum_name': forms.TextInput(attrs={'class': 'form-control'}),
            'kaddum_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'kaddum_sign_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'client_sign_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}), 
        }
        labels={
            'work_area':'*Work Area',
            'record_date':'*Record Date',
            'client_representative':'*Client Representative',
        }

class DayTrackingEmployeeForm(forms.ModelForm):
    employee_total_hours = forms.FloatField(label='Employee Total Hours', required=False)
    employee_id = forms.ModelChoiceField(
    queryset=UserAccount.objects.all(),
    label="*Employee",
    empty_label="Please select...",
    widget=forms.Select(attrs={'class': 'form-control'}),
    error_messages={'required': "This field is mandatory"},
    required=True
    )

    class Meta:
        model = DayTrackingEmployeeDetails
        fields = ('id','employee_id', 'position_id', 'start_time', 'end_time', 'work_description')
        widgets = {
            'position_id': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'work_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_total_hours'].widget.attrs['readonly'] = True
        self.fields['employee_total_hours'].widget.attrs['class'] = 'form-control'
        self.fields['position_id'].choices = [('', 'Please select...')]+[(position.resource_id, position.item_name) for position in ResourceCost.objects.filter(item_type='personel')]



class DayTrackingEquipmentForm(forms.ModelForm):
    equipment_total_hours = forms.FloatField(label='Equipment Total Hours', required=False)
    resource_id = forms.ModelChoiceField(
    queryset=ResourceCost.objects.exclude(item_type = 'personel'),
    label="*Equipment",
    empty_label="Please Select...",
    widget=forms.Select(attrs={'class': 'form-control'}),
    error_messages={'required': "This field is mandatory"},
    )

    class Meta:
        model = DayTrackingEquipmentDetails
        fields=('id','resource_id', 'start_time', 'end_time', 'work_description')
        widgets={
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'work_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipment_total_hours'].widget.attrs['readonly'] = True
        self.fields['equipment_total_hours'].widget.attrs['class'] = 'form-control'


class DayTrackingEmployeeFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra', 1)  # Get 'extra' from kwargs, default to 1 if not provided
        super().__init__(*args, **kwargs)
        self.extra = extra  # Set the extra attribute dynamically
    
    def clean(self):
        if any(self.errors):
            return
        employees = []
        duplicates = False
        
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            employee_id = form.cleaned_data.get('employee_id')
            if employee_id in employees:
                form.add_error('employee_id', 'Employee is duplicated.')
                duplicates = True
            employees.append(employee_id)
        
        if duplicates:
            raise ValidationError("Duplicate employees found in the formset.")

        

class DayTrackingEquipmentFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra', 1)  # Get 'extra' from kwargs, default to 1 if not provided
        super().__init__(*args, **kwargs)
        self.extra = extra  # Set the extra attribute dynamically


DayTrackingEmployeeFormSet = inlineformset_factory(
    DayTracking,
    DayTrackingEmployeeDetails,
    form=DayTrackingEmployeeForm,
    formset=DayTrackingEmployeeFormSet,
     extra=1,

)

DayTrackingEquipmentFormSet = inlineformset_factory(
        DayTracking,
        DayTrackingEquipmentDetails,
        form=DayTrackingEquipmentForm,
        formset=DayTrackingEquipmentFormSet,
        extra=1,
        # min_num=0,
    )
