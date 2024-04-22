from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# Create your models here.

# User = get_user_model()

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        """
        Creates and saves a User with the employee ID,and default password.
        """
        if not username:
            raise ValueError("Users must have a valid EmployeeId")

        # create user model   **kwargs means keyword variable arguments,
        user = self.model(username=username, **kwargs)

        user.set_password(password)  # hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **kwargs):
        """
        Creates and saves a superuser with the given username, and password.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, password=password, **kwargs)


# User Account
class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=6, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True)
    indigenous = models.BooleanField(default=False)
    local = models.BooleanField(default=False)
    position = models.CharField(max_length=50)  # job position
    roles = models.CharField(max_length=50)  # Role permission to access the system

    # we don't change to False because when we create superuser, i won't be able to log in.
    is_active = models.BooleanField(default=True)  # whether user is employeed or not
    is_staff = models.BooleanField(
        default=False
    )  # whether user is allowed to log in the system or not
    is_superuser = models.BooleanField(
        default=False
    )  # whether user is superuser or not

    objects = UserAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "indigenous",
        "local",
        "position",
        "roles",
    ]  # when registering, requried fileds

    def save(self, *args, **kwargs):
        self.full_name = (f"{self.first_name} {self.last_name}") # Combine first and last names

        if not self.username:
            last_record = UserAccount.objects.order_by('-username').first()
            if last_record:
                last_number = int(last_record.username[2:])
                new_number = last_number + 1
                self.username = f"KD{new_number:04d}"
            else:
                self.username = "KD0001"

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
