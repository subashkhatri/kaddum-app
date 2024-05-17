from django.contrib.auth.decorators import user_passes_test


def is_superuser(user):
    return user.is_authenticated and user.roles == "super admin"


def is_supervisor(user):
    return user.is_authenticated and user.roles == "supervisor"


def is_employee(user):
    return user.is_authenticated and user.roles == "employee"

def is_superuser_or_supervisor(user):
    print(f"Checking user: {user}")
    return user.is_authenticated and (user.roles == "super admin" or user.roles == "supervisor")

# Decorator for superuser access
def superuser_required(function=None, redirect_field_name="login", login_url=None):
    actual_decorator = user_passes_test(
        is_superuser, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Decorator for supervisor access
def supervisor_required(function=None, redirect_field_name="login", login_url=None):
    actual_decorator = user_passes_test(
        is_supervisor, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Decorator for employee access
def employee_required(function=None, redirect_field_name="login", login_url=None):
    actual_decorator = user_passes_test(
        is_employee, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Decorator for access by either superuser or supervisor
def superuser_or_supervisor_required(function=None, redirect_field_name="login", login_url=None):
    actual_decorator = user_passes_test(
        is_superuser_or_supervisor,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator