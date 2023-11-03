from .models import Cart, CoffeeItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:   
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            coffeeitem = CoffeeItem.objects.get(pk=item.coffeeitem.id)
            subtotal += (coffeeitem.price * item.quantity) # subtotal = subtotal + (coffeeitem.price * item.quantity)
            

        grand_total = subtotal
    return dict(subtotal=subtotal, grand_total=grand_total)
