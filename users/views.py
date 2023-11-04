from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_decode 
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
import simplejson as json


from .forms import UserForm, UserProfileForm, UserInfoForm
from coffee.forms import CoffeeForm
from .models import User, UserProfile
from coffee.models import Coffee
from orders.models import Order, OrderedCoffee
from . import utils

# def sendemail(request):
    # utils.sendemail()
    # return render(request, 'users/dashboard.html')

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

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'users/emails/account_verification_email.html'
            utils.send_verification_email(request, user, mail_subject, email_template)

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
        return redirect('myAccount')
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
    # print("roleeeeeeeeee", request.user.role)
    # print("roleeeeeeeeee", request.user.first_name)
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'users/customerdashboard.html', {'user': request.user})


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def coffeeDashboard(request):
    # print("coffeeDashboard", request.user)
    # coffee = Coffee.objects.get(user=request.user)
    # print(coffee)
    # return render(request, 'users/coffeedashboard.html', {'coffee': coffee})
    return render(request, 'users/coffeedashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = utils.detectUser(user)
    return redirect(redirectUrl)

def activate(request, uidb64, token):
    # Activate the user by the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send reset password email
            mail_subject = 'Reset your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            utils.send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist.')
            return redirect('forgot_password')
        
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


def clprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            address = profile_form.cleaned_data.get('address')
            if address:
                geo = utils.geocode_address(address)
                if geo:
                    profile.latitude, profile.longitude = geo
                    profile.save()

            messages.success(request, 'Profile updated')
            return redirect('clprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'customers/clprofile.html', context)


def my_orders(request):
    # coffee = Coffee.objects.get(user=request.user)
    # orders = Order.objects.filter(coffees__in=[coffee.id], is_ordered=True).order_by('-created_at')
    email = request.user.email
    orders = Order.objects.filter(email=email, is_ordered=True).order_by('-created_at')
    
    context = {
       'orders': orders,
    }
    return render(request, 'customers/my_orders.html', context)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_coffee = OrderedCoffee.objects.filter(order=order)      
        subtotal = 0
        for item in ordered_coffee:
            subtotal += (item.price * item.quantity)
        context = {
            'order': order,
            'ordered_coffee': ordered_coffee,
            'subtotal': subtotal,
            
        }
        return render(request, 'customers/order_detail.html', context)
    except:
        return redirect('customer')
