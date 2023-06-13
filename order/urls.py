from django.urls import path
from .views import start_order, StripeWebhookView

urlpatterns = [
    path('start_order/', start_order, name='start_order'),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name="stripe-webhook"),
]
