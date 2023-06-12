from django.urls import path
from cart.views import (
    add_to_cart,
    Cart, 
    checkout, 
    HxMenuCart,
    update_cart,
    HxCartTotal,
    Success
    )

urlpatterns = [
    path('', Cart.as_view(), name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('success/', Success.as_view(), name='success'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:action>', update_cart, name="update_cart"),
    path('hx_menu_cart/', HxMenuCart.as_view(), name="hx_menu_cart"),
    path('hx_cart_total/', HxCartTotal.as_view(), name="hx_cart_total"),
] 
