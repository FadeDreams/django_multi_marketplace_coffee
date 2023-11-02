from django.db.models import Prefetch
from django.shortcuts import render
from cat.models import Category
from coffee.models import Coffee
from cat.models import CoffeeItem
from django.shortcuts import get_object_or_404, render

# Create your views here.

def bazaar(request):
    coffees = Coffee.objects.filter(is_approved=True, user__is_active=True)
    # counter rate
    coffee_count = coffees.count()
    context = {
        'coffees': coffees, 
        'coffee_count': coffee_count,
    }
    return render(request, 'bazaar/listing.html', context)

def coffee_detail(request, coffee_slug):
    coffee = get_object_or_404(Coffee, coffee_slug=coffee_slug)
    categories = Category.objects.filter(coffee=coffee).prefetch_related(
        Prefetch('coffeeitem_set', queryset=CoffeeItem.objects.filter())
    )

    context = {
        'categories':categories,
        'coffee': coffee,
    }
    return render(request, 'bazaar/coffee_detail.html', context)
