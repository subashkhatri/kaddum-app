from django.contrib import admin
from.models import UserAccount
# Register your models here.

class ShowAllAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        fields = self.model._meta.fields # Get the fields of the model
        field_names = [field.name for field in fields] # Extract the names of the fields
        return field_names # Return the list of field names

class UserAccountAdmin(admin.ModelAdmin):
  list_display = ('username', 'first_name', 'last_name','position_id','roles','is_indigenous','is_local','is_active','is_staff','is_superuser')


admin.site.register(UserAccount, UserAccountAdmin)