from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from product.models import Product
from .cart import Cart

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return render(request, 'cart/partials/menu_cart.html')

class CartView(TemplateView):
    template_name = 'cart/cart.html'

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action):
    cart = Cart(request)
    if action == "increment":
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)
    
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    if quantity:
        quantity = quantity['quantity']

        item = {
            'product':{
                'id': product_id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    else:
        item = None
        
    response = render(request, 'cart/partials/cart_item.html', {'item':item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'cart/checkout.html', {'pub_key':pub_key})

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')



