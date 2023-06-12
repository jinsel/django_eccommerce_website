from django.urls import path
from django.contrib.auth import views
from core.views import frontpage, signup, shop, MyAccount, edit_myaccount, AboutUs
from product.views import product

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about_us', AboutUs.as_view(), name='about_us'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name="core/login.html"), name='login'),
    path('myaccount/', MyAccount.as_view(), name='myaccount'),
    path('edit_myaccount/', edit_myaccount, name='edit_myaccount'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product, name='product'),
]
