from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from .forms import LoginForm, SignUpForm, CustomPasswordResetForm
from .models import Product, CartItem
from .forms import ProductForm
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
import os
from django.conf import settings
from django.urls import reverse

class Cart:
    _instance = None
    _products = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_product(self, product):
        self._products.append(product)

    def get_products(self):
        return self._products

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('product_list') 
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

class CustomLogoutView(View):
    def get(self, request):
        return render(request, 'logout.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm

@login_required
def product_list(request):
    products = Product.objects.all()
    product_added = request.session.pop('product_added', False)
    return render(request, 'product_list.html', {'products': products, 'product_added': product_added})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product:
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, 'Product added to cart successfully.')
                request.session['product_added'] = True
            else:
                messages.error(request, 'Failed to add product to cart.')
        else:
            pass
    
    return redirect('product_list')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price'] or 0
    
    for cart_item in cart_items:
        cart_item.total_price = cart_item.product.price * cart_item.quantity
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_product(request, product_id):
    cart_item = get_object_or_404(CartItem, product__id=product_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'checkout.html', {'total_price': total_price})

def view_logs(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'app.log')
    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()
    
    return render(request, 'view_logs.html', {'log_content': log_content})

def payment_process(request):
    if request.method == 'POST':
        messages.success(request, "Payment processed successfully.")
        return redirect(reverse('payment_process'))
    
    return render(request, 'payment_process.html')
