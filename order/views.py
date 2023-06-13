import stripe
import json
import time
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Order, OrderItem
from cart.cart import Cart
from product.models import Product

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []
    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        items.append({
            'price_data':{
                'currency': 'inr',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.price * 100,
            },
            'quantity': item['quantity']
        })
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode='payment',
        success_url="http://127.0.0.1:8000/cart/success",
        cancel_url = "http://127.0.0.1:8000/cart"
    )
   
    order = Order.objects.create(user=request.user,
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                email=data['email'],
                                address = data['address'],
                                zipcode=data['zipcode'],
                                place=data['place'],
                                phone=data['phone'],
                                paid=True,
                                paid_amount = total_price * 100
                                )

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        item = OrderItem.objects.create(order=order,
                                        product=product,
                                        price=price,
                                        quantity=quantity)
    cart.clear()
        
    return JsonResponse({
        'session':session,
    })

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(Product, id=product_id)

            send_mail(
                subject="Here is your product",
                message=f"Thanks for your purchase. The URL is: {product.url}",
                recipient_list=[customer_email],
                from_email="test@gmail.com",
            )


        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']
            customer_email = session["customer_details"]["email"]

             # Send an email to the customer asking them to retry their order
            send_mail(
                subject="Payment Failed",
                message="Your Payment is failed. Please retry for payment.",
                recipient_list=[customer_email],
                from_email="test@gmail.com",
            )
        return HttpResponse(status=200)
