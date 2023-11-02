from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from cat.models import Category
from coffee.models import Coffee
from cat.models import CoffeeItem
from .models import Cart
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

def add_to_cart(request, coffee_id):
    print("add_to_cart", coffee_id)
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            # Check if the coffee item exists
            try:
                coffeeitem = CoffeeItem.objects.get(id=coffee_id)
                print("add_to_cart coffeeitem", coffeeitem)
                # Check if the user has already added that coffee to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, coffeeitem=coffeeitem)
                    print("chkCart", chkCart)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity','cart_counter':get_cart_counter(request), 'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, coffeeitem=coffeeitem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the coffee to the cart', 'cart_counter':get_cart_counter(request), 'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This coffee does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart():
    ...

def delete_cart():
    ...
