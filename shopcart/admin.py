from django.contrib import admin

from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user",)

    fields = ["user",]

