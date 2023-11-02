from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CoffeeForm
from users.forms import UserProfileForm

from users.models import UserProfile
from .models import Coffee
from users import utils


# Create your views here.
@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    coffee = get_object_or_404(Coffee, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        coffee_form = CoffeeForm(request.POST, request.FILES, instance=coffee)
        if profile_form.is_valid() and coffee_form.is_valid():
            profile_form.save()
            coffee_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(coffee_form.errors)
    else:     
        profile_form = UserProfileForm(instance=profile)
        coffee_form = CoffeeForm(instance=coffee)
    
    context = {
        'profile_form': profile_form,
        'coffee_form': coffee_form,
        'profile': profile,
        'coffee' : coffee,
    }
    return render(request, 'coffee/cprofile.html', context)
