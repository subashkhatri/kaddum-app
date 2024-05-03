from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required #allow login user to access certain page
from .models import UserAccount
from dashboard.models import *

User = get_user_model()

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'You are not authorized to login.')
        else:
            messages.info(request, 'Invalid credentials')
            # Render the login page again with the error message
            return render(request, 'users/login.html', {'username': username}) # Pass the username back to the template      

    # If the request method is not POST, render the login page
    return render(request, 'users/login.html')
    
def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            messages.info(request, 'User with this username does not exist.')
            return redirect('reset_password')
    else:
        return render(request, 'users/reset_password.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']    
        return render(request, 'users/signup.html')
        # set password criteria
        if password == password2:

            # check if the e-mail exist in the email list
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email registered')
                return redirect('signup')        

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def employees_list(request):
    employee_list = UserAccount.objects.order_by('username')
    return render(request, 'users/employee_list.html', {'employee_list':employee_list})

def employees_add(request):
    positions = ResourceCost.objects.filter(item_type='personel').values_list('item_name', flat=True).distinct()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        indigenous = request.POST['is_indigenous']
        local = request.POST['is_local']
        position = request.POST['position']
        roles = request.POST['role']

        new_employee = UserAccount.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            indigenous = indigenous,
            local = local,
            position = position,
            roles = roles,
        )
        new_employee.save()
        return redirect('employees')

    return render(request, 'users/employee_add.html',{'position_list': positions})