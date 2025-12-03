from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from.models import Order, OrderItem

@login_required
def order_detail(request):
    order = Order.objects.create(
        user = request.user,


    )

    context = {
        "order": order,
    }
    
    return render(request, "general/cart_detail.html", context)
