from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models_resource_cost import ResourceCost
from .models import (
    DayTracking,
    DayTrackingEmployeeDetails,
    DayTrackingEquipmentDetails,
    Project,
    CostTracking,
)
from users.models import UserAccount

class DayTrackingForm(forms.ModelForm):
    kaddum_sign = forms.CharField(widget=forms.HiddenInput(), required=False)
    client_sign = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_draft = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=True)

    record_shift = forms.ChoiceField(
        label="*Record Shift",
        choices=[('', 'Please select...'),('Day Shift', 'Day Shift'),('Night Shift', 'Night Shift')],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    project_no = forms.ModelChoiceField(
        queryset=Project.objects.all().filter(is_active = True).order_by('project_no'),
        label="*Project",
        empty_label="Please select...",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is mandatory"},
        required= True
    )
    class Meta:
        model= DayTracking
        fields = ['project_no','record_date','work_area','client_representative','weather', 'comments', 'kaddum_name','kaddum_sign','kaddum_sign_date','client_name','client_sign','client_sign_date','record_shift','is_draft']
        widgets={
            'record_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'work_area': forms.TextInput(attrs={'class': 'form-control'}),
            'client_representative': forms.TextInput(attrs={'class': 'form-control'}),
            'weather': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'kaddum_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'kaddum_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'kaddum_sign_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'client_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'client_sign_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
        }
        labels={
            'work_area':'*Work Area',
            'record_date':'*Record Date',
            'client_representative':'*Client Representative',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kaddum_sign'].widget = forms.HiddenInput()
        self.fields['client_sign'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        is_draft = cleaned_data.get('is_draft', True) # Default to True if not provided
        project_no = cleaned_data.get('project_no')
        record_date = cleaned_data.get('record_date')
        kaddum_sign_date = cleaned_data.get('kaddum_sign_date')
        client_sign_date = cleaned_data.get('client_sign_date')

        # Check if there is a CostTracking record for the same project and date that is not a draft
        if project_no and record_date:
            cost_tracking_confirmed = CostTracking.objects.filter(
                project_no = project_no,
                record_date = record_date,
                is_draft = False
            ).exists()
            if cost_tracking_confirmed:
                self.add_error('record_date','Please check the record date, as Cost Tracking Record is already confirmed.')

        # Check for required fields when not a draft
        if not is_draft:
            required_fields = [
                'kaddum_name', 'kaddum_sign', 'kaddum_sign_date',
                'client_name', 'client_sign', 'client_sign_date'
            ]
            missing_fields = [field for field in required_fields if not cleaned_data.get(field)]
            if missing_fields:
                for field in missing_fields:
                    self.add_error(field, f"This field is required when submitting.")

            if kaddum_sign_date and kaddum_sign_date < record_date:
                self.add_error('kaddum_sign_date', 'Kaddum sign date cannot be earlier than the record date.')
            if client_sign_date and client_sign_date < record_date:
                self.add_error('client_sign_date', 'Client sign date cannot be earlier than the record date.')

        return cleaned_data


class DayTrackingEmployeeForm(forms.ModelForm):
    employee_total_hours = forms.FloatField(label='Employee Total Hours', required=False)
    employee_id = forms.ModelChoiceField(
    queryset=UserAccount.objects.all().filter(is_active = True).order_by('username'),
    label="*Employee",
    empty_label="Please select...",
    widget=forms.Select(attrs={'class': 'form-control','onchange': 'updatePosition(this);'}),
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
        self.fields['position_id'].choices = [('', 'Please select...')]+[(position.resource_id, position.item_name) for position in ResourceCost.objects.filter(item_type='personnel')]



class DayTrackingEquipmentForm(forms.ModelForm):
    equipment_total_hours = forms.FloatField(label='Equipment Total Hours', required=False)
    resource_id = forms.ModelChoiceField(
    queryset=ResourceCost.objects.exclude(item_type = 'personnel').filter(is_active = True).order_by('item_type'),
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

            # Check for duplicate resource_id
            employee_id = form.cleaned_data.get('employee_id')
            if employee_id:
                # Check for duplicates
                if employee_id in employees:
                    form.add_error('employee_id', 'Employee is duplicated.')
                    duplicates = True
                employees.append(employee_id)

                # Check that start_time and end_time are not the same
                start_time = form.cleaned_data.get('start_time')
                end_time = form.cleaned_data.get('end_time')
                if start_time == end_time:
                    form.add_error('end_time', 'End time cannot be the same as start time.')
            else:
                form.cleaned_data.pop('start_time', None)
                form.cleaned_data.pop('end_time', None)
        if duplicates:
            raise ValidationError("Duplicate employees found in the formset.")
        if not employees:
            form.add_error('employee_id', 'At least one employee is required.')

class DayTrackingEquipmentFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra', 1)  # Get 'extra' from kwargs, default to 1 if not provided
        super().__init__(*args, **kwargs)
        self.extra = extra  # Set the extra attribute dynamically


    def clean(self):
        if any(self.errors):
            return
        equipment = []
        duplicates = False

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            # Check for duplicate resource_id
            resource_id = form.cleaned_data.get('resource_id')
            if resource_id:
                if resource_id in equipment:
                    form.add_error('resource_id', 'Resource is duplicated.')
                    duplicates = True
                equipment.append(resource_id)

                # Check that start_time and end_time are not the same
                start_time = form.cleaned_data.get('start_time')
                end_time = form.cleaned_data.get('end_time')
                if start_time == end_time:
                    form.add_error('end_time', 'End time cannot be the same as start time.')
            else:
                # If resource_id is not selected, remove start_time and end_time from cleaned_data
                form.cleaned_data.pop('start_time', None)
                form.cleaned_data.pop('end_time', None)

        if duplicates:
            raise ValidationError("Duplicate resources found in the formset.")


DayTrackingEmployeeFormSet = inlineformset_factory(
    DayTracking,
    DayTrackingEmployeeDetails,
    form=DayTrackingEmployeeForm,
    formset=DayTrackingEmployeeFormSet,
    can_delete=True,
    # extra=1,

)

DayTrackingEquipmentFormSet = inlineformset_factory(
    DayTracking,
    DayTrackingEquipmentDetails,
    form=DayTrackingEquipmentForm,
    formset=DayTrackingEquipmentFormSet,
    can_delete=True,
    extra=1,
    min_num=0,
    )
