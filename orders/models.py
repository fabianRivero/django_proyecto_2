from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):

    PAYMENT_METHODS = [
        ('card', 'Tarjeta'),
        ('paypal', 'PayPal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name="Método de pago"
    )
    total = models.DecimalField(
        "Total",
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} de {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Pedido"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,   
        verbose_name="Producto"
    )

    product_name = models.CharField("Nombre del producto", max_length=255)
    unit_price = models.DecimalField("Precio unitario", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Cantidad", default=1)
    total_price = models.DecimalField("Subtotal", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Producto del pedido"
        verbose_name_plural = "Productos del pedido"

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Pedido #{self.order.id})"
