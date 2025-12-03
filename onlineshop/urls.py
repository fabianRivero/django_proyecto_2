from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from shopcart.views import add_to_cart, cart_detail, update_cart_item, remove_cart_item, order_confirmation
from .views import ProductListView
from orders.views import OrderListView, OrderDetailView
from profiles.views import RegisterView, LoginView, logout_view

urlpatterns = [
    path('', ProductListView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("shopcart", cart_detail, name="cart_detail"),
    path("update_cart_item/<int:item_id>/", update_cart_item, name="update_cart_item"),
    path("remove_cart_item/<int:item_id>/", remove_cart_item, name="remove_cart_item"),
    path("order_confirmation/", order_confirmation, name="order_confirmation"),
    path("order_record/", OrderListView.as_view(), name="order_record"),
    path("order_record/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path('admin/', admin.site.urls),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
