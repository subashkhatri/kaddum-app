from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        
    class Meta:
        model = Project
        exclude = ['project_no', 'project_total_cost','created_date','last_modification_date']
        widgets = {
            # 'project_no': forms.IntegerField(attrs={'class': 'form-control', 'placeholder': 'Project Number'}),
            'purchase_order_no':forms.TextInput(attrs={'class': 'form-control', }),
            'project_name':forms.TextInput(attrs={'class': 'form-control', }),
            'client':forms.TextInput(attrs={'class': 'form-control', }),
            'project_start_date':forms.DateInput(attrs={'type':'date', 'class': 'form-control', 'placeholder': 'Start Date'}),
            'project_end_date':forms.DateInput(attrs={'type':'date','class': 'form-control', 'placeholder': 'End Date'}),
            'project_budget':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Project Budget'}),
            'is_active':forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Active'), (False, 'Inactive')]),
        }
        labels = {
            'purchase_order_no': 'Purchase Order No',
            'project_name': '*Project Name',
            'client': '*Client',
            'project_start_date': 'Start Date',
            'project_end_date': 'End Date',
            'project_budget': 'Project Budget',
            'is_active': '*Project Status',
        }
