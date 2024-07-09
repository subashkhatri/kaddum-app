from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q, ProtectedError
from django.http import HttpResponse

from .models import UserAccount
from dashboard.models import *
from .forms import UserAccountForm, SuperUserCreationForm
from .decorators import superuser_required, superuser_or_supervisor_required
from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt

User = get_user_model()

# def register_superuser(request):
#     if request.method == 'POST':
#         form = SuperUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Superuser created successfully.')
#             return redirect('admin:index')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = SuperUserCreationForm()

#     return render(request, 'users/register_superuser.html', {'form': form})



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Check user roles for permission to access the system
            if user.roles not in ['supervisor', 'super admin']:
                messages.error(request, "You do not have authorization to log in.")
                return render(request, "users/login.html", {"username": username})

            # User first long in to system
            if user.last_login is None:
                token = jwt.encode({
                    'user_id': user.pk,
                    'exp': datetime.now(timezone.utc) + timedelta(hours=24)
                }, settings.SECRET_KEY, algorithm='HS256')
                reset_url = reverse('reset_password_initial', args=[user.username]) + f"?token={token}"
                return redirect(reset_url)

            # User normally log in
            auth.login(request, user)
            messages.success(request, 'Welcome to Kaddum System!')
            return redirect("/")

        else:
            messages.error(request, "Invalid credentials")
            # Render the login page again with the error message
            return render(
                request, "users/login.html", {"username": username}
            )  # Pass the username back to the template

    return render(request, "users/login.html")

@superuser_required
def reset_password(request):
    if request.method == "POST":
        username = request.POST["username"]
        new_password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been updated successfully!')
                return redirect("employees_list")
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
        except User.DoesNotExist:
            messages.error(request, "User with this username does not exist.")
        return redirect("reset_password")
    else:
        return render(request, "users/reset_password.html")


def reset_password_initial(request, username):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = get_user_model().objects.get(pk=user_id)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, get_user_model().DoesNotExist):
        return HttpResponse("Invalid or expired token.")

    if request.method == "POST":
        new_password = request.POST["password"]
        try:
            validate_password(new_password, user)
            user.set_password(new_password)
            user.last_login = datetime.now(timezone.utc)
            user.save(update_fields=['password', 'last_login'])
            messages.success(request, 'Your password has been updated successfully!')
            return redirect("login")
        except ValidationError as e:
            for message in e.messages:
                messages.error(request, message)
        except get_user_model().DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, "users/reset_password_intial.html", {'user': user})


def logout(request):
    auth.logout(request)
    return redirect("login")

@superuser_or_supervisor_required
def employees_list(request):
    query = request.GET.get('q', '').strip().lower()
    if query:
        is_indigenous_query = {'indigenous': True, 'no': False}.get(query, None)
        is_local_query = {'local': True, 'no': False}.get(query, None)
        is_active_query = {'active': True, 'inactive': False}.get(query, None)

        employees = UserAccount.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(roles__icontains=query)|
            (Q(is_indigenous=is_indigenous_query) if is_indigenous_query is not None else Q())|
            (Q(is_local=is_local_query) if is_local_query is not None else Q())|
            (Q(is_active=is_active_query) if is_active_query is not None else Q())
        ).order_by('-username')
    else:
        employees = UserAccount.objects.all().order_by('-username')

    paginator = Paginator(employees, 10)  # Show 10 records per page.
    page_number = request.GET.get('page')
    employee_list  = paginator.get_page(page_number)
    return render(request, "users/employee_list.html", {"employee_list": employee_list})

@superuser_or_supervisor_required
def employee_add(request):
    if request.method == "POST":
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect("employees_list")
    else:
        form = UserAccountForm()

    return render(request, "users/employee_create.html", {"form": form})

@superuser_or_supervisor_required
def employee_edit(request, username):
    employee = get_object_or_404(UserAccount, pk=username)
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = UserAccountForm(request.POST, instance=employee)
        if form.is_valid():
            # Save the updated employee details
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect(
                "employees_list"
            )
    else:
        form = UserAccountForm(instance=employee)

    return render(request, "users/employee_edit.html", {"form": form, 'employee':employee})

@superuser_or_supervisor_required
def employee_delete(request, username):
    employee = get_object_or_404(UserAccount, pk=username)
    if request.method == 'POST':
        try:
            employee.delete()
            messages.success(request, 'User account has been deleted successfully.')
            return redirect('employees_list')
        except ProtectedError as e:
            # Extracting information from the ProtectedError
            message = f"Cannot delete this employee because '{employee}' is referenced by other records. Please set the employee status to inactive."
            messages.error(request, message)
            return redirect('employees_list')  # Redirect to the list or some error page

    return render(request, 'users/confirm_delete.html', {'employee': employee})
