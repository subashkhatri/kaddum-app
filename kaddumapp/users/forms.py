from django import forms
from .models import UserAccount
from dashboard.models_resource_cost import ResourceCost


class SuperUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Re-Type Your Password"}
        ),
    )

    class Meta:
        model = UserAccount
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_indigenous",
            "is_local",
            "roles",
            "is_active",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "is_indigenous": forms.Select(
                attrs={"class": "form-control"},
                choices=[("", "Please select..."), ("True", "Yes"), ("False", "No")],
            ),
            "is_local": forms.Select(
                attrs={"class": "form-control"},
                choices=[("", "Please select..."), (True, "Yes"), (False, "No")],
            ),

            "roles": forms.Select(
                attrs={"class": "form-control"},
                choices=[
                    ("", "Please select..."),
                    ("super admin", "Super Admin"),
                    ("supervisor", "Supervisor"),
                    ("restricted user", "Restricted User"),
                ],
            ),
            "is_active": forms.Select(
                attrs={"class": "form-control"},
                choices=[(True, "Active"), (False, "Inactive")],
            ),
        }
        labels = {
            "first_name": "*First Name",
            "last_name": "*Last Name",
            "email": "*Email",
            "is_indigenous": "*Indigenous",
            "is_local": "*Local",
            "position_id": "*Position",
            "roles": "*System Role",
            "is_active": "*Employeement Status",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_superuser = True
        user.is_staff = True
        if "position_id" in self.cleaned_data:
            user.position_id = ResourceCost.objects.get(
                resource_id=self.cleaned_data["position_id"]
            )
        if commit:
            user.save()
        return user


class UserAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        positions = ResourceCost.objects.filter(item_type="personel").values_list(
            "resource_id", "item_name"
        )
        self.fields["position_id"].choices = [("", "Please select...")] + list(
            positions
        )

    class Meta:
        model = UserAccount
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_indigenous",
            "is_local",
            "position_id",
            "roles",
            "is_active",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "is_indigenous": forms.Select(
                attrs={"class": "form-control"},
                choices=[("", "Please select..."), ("True", "Yes"), ("False", "No")],
            ),
            "is_local": forms.Select(
                attrs={"class": "form-control"},
                choices=[("", "Please select..."), (True, "Yes"), (False, "No")],
            ),
            "position_id": forms.Select(attrs={"class": "form-control"}),
            "roles": forms.Select(
                attrs={"class": "form-control"},
                choices=[
                    ("", "Please select..."),
                    ("super admin", "Super Admin"),
                    ("supervisor", "Supervisor"),
                    ("employee", "Employee"),
                ],
            ),
            "is_active": forms.Select(
                attrs={"class": "form-control"},
                choices=[(True, "Active"), (False, "Inactive")],
            ),
        }
        labels = {
            "first_name": "*First Name",
            "last_name": "*Last Name",
            "email": "*Email",
            "is_indigenous": "*Indigenous",
            "is_local": "*Local",
            "position_id": "*Position",
            "roles": "*System Role",
            "is_active": "*Employeement Status",
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.instance.pk:  # Checking if it's a new instance
            user.set_password(self.cleaned_data.get('password', 'kaddum123'))
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        position_id = cleaned_data.get('position_id')

        # Check if position_id is required (i.e., for non-superusers)
        if not self.instance.is_superuser and not position_id:
            raise forms.ValidationError("Position ID is required for all non-superuser accounts.")

        return cleaned_data

