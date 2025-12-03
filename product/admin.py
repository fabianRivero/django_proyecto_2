from django.contrib import admin

from .models import Category, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    list_filter = ("category", "stock", "is_active")

    fields = ["name", "description", "category", "price", "stock", "image", "is_active"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("name", "slug")

    fields = ["name", "slug"]
