from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import (
    login_required,
)  # allow login user to access certain page
from .models import UserAccount
from dashboard.models import *
from .forms import UserAccountForm, SuperUserCreationForm
# from django.contrib.auth.decorators import user_passes_test

User = get_user_model()

def superuser_required(user):
    return user.is_authenticated and user.is_superuser

# @user_passes_test(superuser_required)
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
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "You are not authorized to login.")
        else:
            messages.info(request, "Invalid credentials")
            # Render the login page again with the error message
            return render(
                request, "users/login.html", {"username": username}
            )  # Pass the username back to the template

    # If the request method is not POST, render the login page
    return render(request, "users/login.html")


def reset_password(request):
    if request.method == "POST":
        username = request.POST["username"]
        new_password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect("login")
        except User.DoesNotExist:
            messages.info(request, "User with this username does not exist.")
            return redirect("reset_password")
    else:
        return render(request, "users/reset_password.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        return render(request, "users/signup.html")
        # set password criteria
        if password == password2:

            # check if the e-mail exist in the email list
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email registered")
                return redirect("signup")


# @login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


def employees_list(request):
    employee_list = UserAccount.objects.order_by("username")
    return render(request, "users/employee_list.html", {"employee_list": employee_list})


def employee_add(request):
    if request.method == "POST":
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employees_list")
    else:
        form = UserAccountForm()

    return render(request, "users/employee_add.html", {"form": form})


def employee_update(request, employee_id):
    employee = get_object_or_404(UserAccount, username=employee_id)
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = UserAccountForm(request.POST, instance=employee)
        if form.is_valid():
            # Save the updated employee details
            form.save()
            # Redirect to a success page or display a success message
            return redirect(
                "employees_list"
            )  # Assuming you have a URL name for the employees list page
    else:
        # Create a form instance and populate it with the existing employee data
        form = UserAccountForm(instance=employee)

    return render(request, "users/employee_edit.html", {"form": form})
