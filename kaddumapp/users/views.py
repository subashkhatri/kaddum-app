from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required #allow login user to access certain page

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