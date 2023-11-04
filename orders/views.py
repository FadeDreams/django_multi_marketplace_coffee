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

from core.settings import settings
from django.views.decorators.csrf import csrf_exempt
import stripe

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
    return render(request,  'bazaar/cart.html')


def order_complete(request):
    # order_number = request.GET.get('order_no')
    # transaction_id = request.GET.get('trans_id')
    session_id = request.GET.get('session_id')  # Add this line to get session_id
    payment = Payment.objects.get(transaction_id=session_id)

    try:
        order = Order.objects.get(payment=payment)
        order.status = 'Accepted'
        order.save()
        
        orderedcoffee = OrderedCoffee.objects.filter(order=order)

        subtotal = 0
        for item in orderedcoffee:
            subtotal += (item.price * item.quantity)

        context = {
            'order': order,
            'ordered_coffee': orderedcoffee,
            'subtotal': subtotal,
            'session_id': session_id  # Add session_id to the context
        }
        # return render(request, 'orders/success.html')  # Replace 'yourapp' with your app name
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')



def payments(request):
    ...

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, order_number):
    # print(order_number)
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        order = Order.objects.get(order_number=order_number)
        amount = int(order.total)  # Replace with the actual field that stores the amount
        coffee_count = order.coffees.count()
        if coffee_count < 1:
            coffee_count = 1
        # print(amount)
        email = order.email  # Replace with the actual field that stores the amount

        try:
            # For full details see https://stripe.com/docs/api/checkout/sessions/create
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'coffee_payment',
                        'currency': 'usd',
                        'quantity': coffee_count,
                        'amount': amount,
                    }
                ]
            )
            print("checkout session", checkout_session['id'])
            payment = Payment( user = request.user, transaction_id = checkout_session['id'], payment_method = 'Stripe',
                amount = order.total, status = 'New'
            )
            payment.save()
            # Update the order model
            order.payment = payment
            # order.payment.transaction_id = checkout_session['id']
            order.is_ordered = True
            order.save()
            # Move the Cart items to ordered coffee model
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                ordered_coffee = OrderedCoffee()
                ordered_coffee.order = order
                ordered_coffee.payment = payment
                ordered_coffee.user = request.user
                ordered_coffee.coffeeitem = item.coffeeitem
                ordered_coffee.quantity = item.quantity
                ordered_coffee.price = item.coffeeitem.price
                ordered_coffee.amount = item.coffeeitem.price * item.quantity # total amount
                ordered_coffee.save()


            return JsonResponse({'sessionId': checkout_session['id']})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    if request.method == 'POST':
        # Your code to create a checkout session here
        try:
            # Create the checkout session
            checkout_session = stripe.checkout.Session.create(
                # Your checkout session parameters here
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# def successview(request):
    # return render(request, 'orders/success.html')  # Replace 'yourapp' with your app name

def cancelview(request):
    return render(request, 'orders/cancel.html')  # Replace 'yourapp' with your app name


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)
