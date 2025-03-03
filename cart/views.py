from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sabji.models import Product
from .models import Cart

# Create your views here.



@login_required
def add_to_cart(request, id, quantity):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product)
    if cart.exists():
        cart = cart.first()
        cart.active = True
        cart.quantity += quantity
        cart.save()
    else:
        cart = Cart(user=user, product=product, quantity=quantity)
        cart.save()
    return render(request, 'cart/cart_count.html',{'cart_count':Cart.objects.filter(user=user,active=True).count()})

@login_required
def increase_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product,active=True)
    if cart.exists():
        cart.active = True
        cart = cart.first()
        cart.quantity += 1
        cart.save()
    total = 0
    carts = Cart.objects.filter(user=user,active=True)
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 00,
    }

    return render(request, 'cart/cart_checkout.html',context)

@login_required
def decrease_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product)
    if cart.exists():
        cart.active = True
        cart = cart.first()
        cart.quantity -= 1
        cart.save()
    total = 0
    carts = Cart.objects.filter(user=user,active=True)
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 00,
    }
    return render(request, 'cart/cart_checkout.html',context)


def cart(request):
    carts = Cart.objects.filter(user=request.user,active=True)
    print("Cart Items:", carts) 
    total = 0
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 00,
        'cart': carts
    }
    return render(request,'cart/cart.html',context)

def checkout(request):
    carts = Cart.objects.filter(user=request.user,active=True)
    total = 0
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 00, 
        'carts': carts
    }
    return render(request,'cart/checkout.html',context)

@login_required
def remove_from_cart(request, id, quantity):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product, quantity=quantity)
    cart.delete()
    carts = Cart.objects.filter(user=request.user)
    total = 0
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 00,
    }
    return render(request,'cart/cart_checkout.html',context)