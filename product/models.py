from django.db import models

class Category(models.Model):
    name = models.CharField("Nombre", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Categoría", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", blank=True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Stock", default=0)
    image = models.ImageField("Imagen de producto", upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name