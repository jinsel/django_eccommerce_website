from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from product.models import Product, Category
from .forms import SignUpForm

def frontpage(request):
    products = Product.objects.all()[:8]
    context={
        'products':products
    }

    return render(request, 'core/frontpage.html', context)

def about_us(request):
    return render(request,  'core/about_us.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    
    context = {
        'form': form
    }
    return render(request, 'core/signup.html', context)

@login_required
def my_account(request):
    return render(request, 'core/myaccount.html')

@login_required
def edit_myaccount(request):
    if request.method == "POST":
        user= request.user
        user.first_name = request.POST.get('first_name')
        user.last_name =  request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('myaccount')
        
    return render(request, 'core/edit_myaccount.html')

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    if query := request.GET.get('query', ''):
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }

    return render(request, 'core/shop.html', context)