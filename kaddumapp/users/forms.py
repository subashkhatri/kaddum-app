from django import forms
from .models import UserAccount
from dashboard.models_resource_cost import ResourceCost

True_False_CHOICES = [
        ('', "Please select..."),
        (True, 'Yes'),
        (False, 'No'),
    ]

class UserAccountForm(forms.ModelForm):
        
    is_indigenous = forms.ChoiceField(
    label="*Indigenous",
    choices = True_False_CHOICES,
    widget=forms.Select(attrs={'class': 'form-control'}),
    error_messages={'required': "This field is mandatory"}
    )

    is_local = forms.ChoiceField(
    label="*Local",
    choices = True_False_CHOICES,
    widget=forms.Select(attrs={'class': 'form-control'}),
    error_messages={'required': "This field is mandatory"}
    )
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'email', 'is_indigenous', 'is_local', 'position_id', 'roles', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'},),
            'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'position_id': forms.Select(attrs={'class': 'form-control'}),           
            'roles': forms.Select(attrs={'class': 'form-control'},choices=[('','Please select...'),('super admin', 'Super Admin'),('supervisor', 'Supervisor'),('restricted user', 'Restricted User')]),
            'is_active':forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Active'), (False, 'Inactive')]),
        }
        labels = {
            'first_name': '*First Name',
            'last_name': '*Last Name',
            'email': '*Email',
            'is_indigenous': '*Indigenous',
            'is_local': '*Local',
            'position_id': '*Position',
            'roles': '*System Role',
            'is_active': '*Employeement Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        positions = ResourceCost.objects.filter(item_type='personel').values_list('resource_id', 'item_name')
        self.fields['position_id'].choices = [('', 'Please select...')] + list(positions)
        