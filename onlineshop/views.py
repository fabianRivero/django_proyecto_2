from django.views.generic import ListView
from django.db.models import Q
from django.views.generic.edit import FormMixin
from product.models import Product, Category
from product.forms import ProductFilterForm


class ProductListView(FormMixin, ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'
    form_class = ProductFilterForm        
    paginate_by = 9     

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.GET or None
        kwargs["categories"] = Category.objects.all()
        return kwargs               

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category')
     
        form = self.get_form()

        if form.is_valid():
            search = form.cleaned_data.get("search")
            category = form.cleaned_data.get("category")

            if category:
                qs = qs.filter(category=category)

            if search:
                qs = qs.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )

        return qs.order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = self.get_form()
        return ctx