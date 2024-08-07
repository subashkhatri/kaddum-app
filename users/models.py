from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from dashboard.models_resource_cost import ResourceCost

# Create your models here.

# User = get_user_model()

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        """
        Creates and saves a User with the employee ID,and default password.
        """
        if not username:
            raise ValueError("Users must have a valid EmployeeId")

        if 'position_id' in kwargs and isinstance(kwargs['position_id'], int):
            kwargs['position_id'] = ResourceCost.objects.get(pk=kwargs['position_id'])
        # create user model   **kwargs means keyword variable arguments,
        user = self.model(username=username, **kwargs)
        if not password:
            password = "Kaddum2024"

        user.set_password(password)  # hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **kwargs):
        """
        Creates and saves a superuser with the given username, and password.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
       # Superuser does not need a position_id
        kwargs.pop('position_id', None)

        return self.create_user(username=username, password=password, **kwargs)


# User Account
class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=6, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_indigenous = models.BooleanField(null=False, blank=False)
    is_local = models.BooleanField(null=False, blank=False)
    position_id = models.ForeignKey(ResourceCost, on_delete=models.PROTECT, db_column='position_id', null=True, blank=True) # job position
    roles = models.CharField(max_length=50, blank=True, default='employee')  # Role permission to access the system super_admin, supervisor, restricted user

    # we don't change to False because when we create superuser, i won't be able to log in.
    is_active = models.BooleanField(default=True)  # whether user is employeed or not
    is_staff = models.BooleanField(default=False)  # whether user is allowed to log in the system or not
    is_superuser = models.BooleanField(default=False)  # whether user is superuser or not

    objects = UserAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        'email',
        "is_indigenous",
        "is_local",
        "roles",
    ]  # when registering, requried fileds
    class Meta:
        app_label = 'users'
        db_table = 'users-UserAccount'

    def save(self, *args, **kwargs):
        self.full_name = (f"{self.first_name} {self.last_name}") # Combine first and last names

        if not self.username:
            last_record = UserAccount.objects.order_by('-username').first()
            if last_record:
                prefix = last_record.username[:2]
                suffix = last_record.username[2:]

                # Check if the suffix is numeric and increment
                if suffix.isdigit():
                    last_number = int(suffix)
                    new_number = last_number + 1
                    self.username = f"{prefix}{new_number:04d}"
                else:
                    # Fallback if no suitable last record is found
                    self.username = "KD0001"  # Default to start from 'KD0001' if unable to parse
            else:
                self.username = "KD0001"

        super().save(*args, **kwargs)


    def __str__(self):
        return self.full_name
