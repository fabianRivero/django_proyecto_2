from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "general/order_record.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items") 
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "general/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
