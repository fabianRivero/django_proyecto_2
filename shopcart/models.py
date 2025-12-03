from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito de {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name="Carrito", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, verbose_name="Producto", on_delete=models.CASCADE)
    quantity = models.IntegerField("Cantidad", default=1)
    unit_price = models.DecimalField("Precio de unidad", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("Precio total", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Producto del carrito'
        verbose_name_plural = 'Productos del carrito'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"