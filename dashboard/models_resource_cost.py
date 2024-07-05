from django.db import models


class ResourceCost(models.Model):
    resource_id = models.AutoField(primary_key= True)
    item_type = models.CharField(max_length=30)
    item_name = models.CharField(max_length=255)
    item_id = models.CharField(max_length=10, null=True, blank=True)
    item_location = models.CharField(max_length=30, null=True, blank=True)
    item_rate = models.FloatField(default=0)
    unit_of_measure = models.CharField(max_length=10)
    mobilisation_desc = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dashboard'
        db_table = 'dashboard-ResourceCost'

    def __str__(self):
        if self.item_id:
            return f"{self.item_type.capitalize()}-{self.item_id.upper()}-{self.item_name}"
        return f"{self.item_type.capitalize()}-{self.item_name}"
