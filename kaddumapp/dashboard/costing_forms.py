from django import forms
from .models import CostTracking, Project, UserAccount

SHIFT_CHOICES = [
    ('morning', 'Morning'),
    ('night', 'Night'),
]

def validate_non_negative(value):
    if value < 0:
        raise forms.ValidationError("The quantity cannot be less than 0.")

class CostTrackingForm(forms.ModelForm):
    day_of_week = forms.CharField(required=False, label="Day", widget=forms.TextInput(attrs={'readonly': 'readonly'}))


    def get_day_of_week(self):
        # Calculate day of week from the record_date
        record_date = self.cleaned_data.get('record_date')
        if record_date:
            return record_date.strftime('%A')  # Returns the full weekday name
        return ""

    class Meta:
        model = CostTracking
        # fields = '__all__'  # Adjust as necessary to exclude specific fields
        exclude = ['project_no', 'cost_tracking_id', 'year_week', 'created_date', 'last_modification_date', 'is_draft'] 
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # 'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'total_hours_indigenous': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_hours_local': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(CostTrackingForm, self).__init__(*args, **kwargs)
        quantity_fields = ['total_hours']
        self.fields['day_of_week'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
        if self.instance and self.instance.record_date:
            self.fields['day_of_week'].initial = self.instance.record_date.strftime('%A')

        for field_name in quantity_fields:
            self.fields[field_name].validators.append(validate_non_negative)
            self.fields[field_name].widget.attrs.update({'min': '0', 'class': 'form-control'})  # Set the minimum value to 0 for frontend validation
