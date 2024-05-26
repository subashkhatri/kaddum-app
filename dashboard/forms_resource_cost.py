# resource_cost_forms.py
from django import forms
from .models import ResourceCost

class ResourceCostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceCostForm, self).__init__(*args, **kwargs)
        # Disable the last_modification_date field to prevent it from being edited
        if 'last_modification_date' in self.fields:
            self.fields['last_modification_date'].disabled = True


    class Meta:
        model = ResourceCost
        fields = '__all__'  # Includes all fields, you can exclude fields if necessary
        widgets = {
            'item_type': forms.TextInput(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_id': forms.TextInput(attrs={'class': 'form-control'}),
            'item_location': forms.TextInput(attrs={'class': 'form-control'}),
            'item_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_of_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'mobilisation_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'item_type': '*Item Type',
            'item_name': '*Item Name',
            'item_id': 'Item ID',
            'item_location': 'Location',
            'item_rate': '*Cost Rate',
            'unit_of_measure': '*Unit of Measure',
            'mobilisation_desc': 'Mobilisation Description',
        }


    def clean_last_modification_date(self):
        return self.instance.last_modification_date if self.instance else None

    def clean_item_rate(self):
        item_rate = self.cleaned_data.get('item_rate')
        if item_rate <= 0:
            raise forms.ValidationError('Item rate cannot be negative.')
        return item_rate