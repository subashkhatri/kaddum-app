from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from .models import UserAccount
from dashboard.models import *
from .forms import UserAccountForm, SuperUserCreationForm
from .decorators import superuser_required, supervisor_required, employee_required


User = get_user_model()

@superuser_required
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


def employees_list(request):
    employee_list = UserAccount.objects.order_by("username")
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

    return render(request, "users/employee_add.html", {"form": form})

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
