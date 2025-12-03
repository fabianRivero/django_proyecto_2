from shopcart.models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = request.user.cart            
            count = sum(item.quantity for item in cart.items.all())

        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0

    return {
        "cart_item_count": count
    }
