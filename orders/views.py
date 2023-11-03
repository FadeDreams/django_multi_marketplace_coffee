from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from bazaar.models import Cart
from bazaar.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order, Payment, OrderedCoffee
import simplejson as json
from .utils import generate_order_number, order_total_by_coffee
from users.utils import send_notification
from django.contrib.auth.decorators import login_required
from cat.models import CoffeeItem
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction

from django.db import transaction

@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('bazaar')
    
    coffees_ids = []
    for i in cart_items:
        if i.coffeeitem.coffee.id not in coffees_ids:
            coffees_ids.append(i.coffeeitem.coffee.id)
            
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        coffeeitem = CoffeeItem.objects.get(pk=i.coffeeitem.id, coffee_id__in=coffees_ids)
        v_id = coffeeitem.coffee.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (coffeeitem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (coffeeitem.price * i.quantity)
            k[v_id] = subtotal

        total_data.update({coffeeitem.coffee.id: {str(subtotal)}}) 
    print(total_data)
            
    grand_total = get_cart_amounts(request)['grand_total']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order()
                order.first_name = form.cleaned_data['first_name']
                order.last_name = form.cleaned_data['last_name']
                order.phone = form.cleaned_data['phone']
                order.email = form.cleaned_data['email']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.state = form.cleaned_data['state']
                order.city = form.cleaned_data['city']
                order.pin_code = form.cleaned_data['pin_code']
                order.user = request.user
                order.payment_method = request.POST['payment_method']
                order.total = grand_total  # Set the total field
                order.save()  # order id/pk is generated 
                order.order_number = generate_order_number(order.id)
                order.coffees.add(*coffees_ids)
                order.save()

                context = {
                    'order': order,
                    'cart_items': cart_items,
                }
                return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request,  'orders/place_order.html')


def order_complete(request):
    ...

def payments(request):
    ...
