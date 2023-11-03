from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from cat.models import Category
from coffee.models import Coffee
from cat.models import CoffeeItem
from .models import Cart
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from users.models import UserProfile
from orders.forms import OrderForm


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

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'categories':categories,
        'coffee': coffee,
        'cart_items':cart_items,
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
                print("in try")
                try:
                    print("request.user", request.user)
                    chkCart = Cart.objects.get(user=request.user, coffeeitem=coffeeitem)
                    print("chkCart", chkCart)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success',
                                         'message': 'Increased the cart quantity',
                                         'cart_counter':get_cart_counter(request),
                                         'qty':chkCart.quantity,
                                         'cart_amount':get_cart_amounts(request)})
                except:
                    print("failed try")
                    chkCart = Cart.objects.create(user=request.user, coffeeitem=coffeeitem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the coffee to the cart', 'cart_counter':get_cart_counter(request), 'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This coffee does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, coffee_id):
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with')=='XMLHttpRequest':
                # Check if the coffee item exists
                try:
                    coffeeitem = CoffeeItem.objects.get(id=coffee_id)
                    # Check if the user has already added that coffee to the cart
                    try:
                        chkCart = Cart.objects.get(user=request.user, coffeeitem=coffeeitem)
                        if chkCart.quantity > 1:
                            # Decrease the cart quantity
                            chkCart.quantity -= 1
                            chkCart.save()
                        else:
                            chkCart.delete()    
                            chkCart.quantity = 0
                        return JsonResponse({'status': 'Success','cart_counter':get_cart_counter(request), 'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
                    except:
                        return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This coffee does not exist!'})
            else:
                return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        else:
            return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message': 'Cart Item has been deleted!' ,'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Cart Item does not exist!'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid request!'})



@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'bazaar/cart.html', context)


@login_required(login_url='login')  
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('bazaar')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,  
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'bazaar/checkout.html', context)

