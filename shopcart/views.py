from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from product.models import Product
from .models import Cart, CartItem
from orders.models import Order, OrderItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price for item in items)

    context = {
        "cart": cart,
        "items": items,
        "total": total,
    }
    return render(request, "general/cart_detail.html", context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "quantity": 1,
            "unit_price": product.price,
            "total_price": product.price,
        }
    )

    if not item_created:
        new_q = cart_item.quantity + 1

        if product.stock > new_q:
            cart_item.quantity = new_q
            cart_item.total_price = cart_item.unit_price * new_q
            cart_item.save()
        else:
            messages.add_message(request, messages.ERROR, f"Solo hay {product.stock} unidades de '{product.name}' disponibles.")        


    messages.add_message(request, messages.SUCCESS, f"{product.name} fue añadido al carrito.")
    return redirect("home")

@login_required
def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "plus":
            new_q = item.quantity + 1
            if new_q <= item.product.stock:
                item.quantity = new_q
                item.total_price = item.unit_price * new_q
                item.save()
            else:
                messages.add_message(request, messages.ERROR, f"No hay suficiente stock de '{item.product.name}'. Stock disponible: {item.product.stock}.")    

        elif action == "minus":
            new_q = item.quantity - 1
            if new_q > 0:
                item.quantity = new_q
                item.total_price = item.unit_price * new_q
                item.save()
            else:
                item.delete()

    return redirect("cart_detail")

@login_required
def remove_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        item.delete()

        messages.add_message(request, messages.INFO, f"Se eliminó '{item.product.name}' del carrito.")

    return redirect("cart_detail")


@login_required
def order_confirmation(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items:
        messages.add_message(request, messages.ERROR, "Tu carrito está vacío.")
        return redirect("cart_detail")

    total = sum(item.total_price for item in items)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        card_number = request.POST.get("card_number")
        card_name = request.POST.get("card_name")
        paypal_email = request.POST.get("paypal_email")

        if payment_method == "card":
            if not card_number or not card_name:
                messages.add_message(request, messages.ERROR, "Completa los datos de la tarjeta.")
                return render(
                    request,
                    "general/order_confirmation.html",
                    {"cart": cart, "items": items, "total": total},
                )
        elif payment_method == "paypal":
            if not paypal_email:
                messages.add_message(request, messages.ERROR, "Ingresa el correo de PayPal.")      
                return render(
                    request,
                    "general/order_confirmation.html",
                    {"cart": cart, "items": items, "total": total},
                )

        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            total=total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=item.total_price,
            )

        items.delete()

        messages.add_message(request, messages.SUCCESS, "Pago realizado correctamente. ¡Gracias por tu compra!")
        return redirect("cart_detail")

    context = {
        "cart": cart,
        "items": items,
        "total": total,
    }
    return render(request, "general/order_confirmation.html", context)