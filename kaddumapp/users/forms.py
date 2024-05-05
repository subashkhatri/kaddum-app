from django import forms
from .models import UserAccount
from dashboard.models_resource_cost import ResourceCost

class UserAccountForm(forms.ModelForm):
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        positions = ResourceCost.objects.filter(item_type='personel').values_list('resource_id', 'item_name')
        self.fields['position_id'].choices = [('', 'Please select...')] + list(positions)
        
        
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'email', 'is_indigenous', 'is_local', 'position_id', 'roles', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_indigenous':forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Please select...'), ('True', 'Yes'), ('False', 'No')],),
            'is_local':forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Please select...'), (True, 'Yes'), (False, 'No')]),
            'position_id': forms.Select(attrs={'class': 'form-control'}),           
            'roles': forms.Select(attrs={'class': 'form-control'},choices=[('','Please select...'),('Super Admin', 'super admin'),('Supervisor', 'supervisor'),('Restricted User', 'restricted user')]),
            'is_active':forms.Select(attrs={'class': 'form-control'}, choices=[('True', 'Yes'), ('False', 'No')]),
        }
        labels = {
            'first_name': '*First Name',
            'last_name': '*Last Name',
            'email': '*Email',
            'is_indigenous': '*Indigenous',
            'is_local': '*Local',
            'position_id': '*Position',
            'roles': '*System Role',
            'is_active': '*In Employeement',
        }
