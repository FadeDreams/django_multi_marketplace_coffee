from django.shortcuts import get_object_or_404, render
from .forms import CoffeeForm
from users.forms import UserProfileForm

from users.models import UserProfile
from .models import Coffee

# Create your views here.
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    coffee = get_object_or_404(Coffee, user=request.user)
    
    profile_form = UserProfileForm(instance=profile)
    coffee_form = CoffeeForm(instance=coffee)
    
    context = {
        'profile_form': profile_form,
        'coffee_form': coffee_form,
        'profile': profile,
        'coffee' : coffee,
    }
    return render(request, 'coffee/vprofile.html', context)
