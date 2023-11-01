import sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import UserForm
from coffee.forms import CoffeeForm
from .models import User, UserProfile
from . import utils


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been  registered successfully!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'users/registerUser.html', context)

def registerCoffee(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = CoffeeForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.COFFEE
            user.save()
            coffee = v_form.save(commit=False)
            coffee.user = user
            user_profile = UserProfile.objects.get(user=user)
            coffee.user_profile = user_profile
            coffee.save()
            
            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'users/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            # messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            # return redirect ('registercoffee')
        else:
            # print('invalid form')
            print(form.errors)
        
    else:
        form = UserForm()
        v_form = CoffeeForm()
    
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'users/registerCoffee.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        print(email)
        print(password)
        print(user)
        
        if user is not None:
            print("user is not None")
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'users/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(utils.check_customer_role)
def userDashboard(request):
    return render(request, 'users/dashboard.html')

@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def coffeeDashboard(request):
    return render(request, 'users/dashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = utils.detectUser(user)
    return redirect(redirectUrl)
