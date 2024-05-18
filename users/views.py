from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

from .models import UserAccount
from dashboard.models import *
from .forms import UserAccountForm, SuperUserCreationForm
from .decorators import superuser_required, superuser_or_supervisor_required



User = get_user_model()

def register_superuser(request):
    if request.method == 'POST':
        form = SuperUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Superuser created successfully.')
            return redirect('admin:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SuperUserCreationForm()

    return render(request, 'users/register_superuser.html', {'form': form})



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome to Kaddum App!')
            return redirect("/")

        else:
            messages.info(request, "Invalid credentials")
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
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been updated successfully!')
            return redirect("login")
        except User.DoesNotExist:
            messages.info(request, "User with this username does not exist.")
            return redirect("reset_password")
    else:
        return render(request, "users/reset_password.html")


def logout(request):
    auth.logout(request)
    return redirect("login")

@superuser_required
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

@superuser_required
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

@superuser_required
def employee_edit(request, employee_id):
    employee = get_object_or_404(UserAccount, username=employee_id)
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

    return render(request, "users/employee_edit.html", {"form": form})

def delete_employee(request, username):
    user = get_object_or_404(UserAccount, username=username)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User account has been deleted successfully.')
        return redirect('employees_list')
    return render(request, 'users/confirm_delete.html', {'user': user})
