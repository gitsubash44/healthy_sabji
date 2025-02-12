from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sabji.models import Product
from .models import Cart


# Create your views here.


'''
    TODO: 
    1. in Checkout Page, remove the Cart from the topbar
    2. Whenever a user clicks on the plus,minus or remove button, the whole table along with the total section should be updates as a component.
'''
@login_required
def add_to_cart(request, id, quantity):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product)
    if cart.exists():
        cart = cart.first()
        cart.quantity += quantity
        cart.save()
    else:
        cart = Cart(user=user, product=product, quantity=quantity)
        cart.save()
   
    return render(request, 'cart/cart_count.html')

@login_required
def increase_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product)
    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
    total = 0
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 50,
    }

    return render(request, 'cart/cart_checkout.html',context)

@login_required
def decrease_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    cart = Cart.objects.filter(user=user, product=product)
    if cart.exists():
        cart = cart.first()
        cart.quantity -= 1
        cart.save()
    total = 0
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 50,
    }
    return render(request, 'cart/cart_checkout.html',context)


def cart(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 50,
    }
    return render(request,'cart/cart.html',context)

def checkout(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    for cart in carts:
        total += cart.product.price * cart.quantity
    context = {
        'total': total,
        'shipping': 50,
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
        'shipping': 50,
    }
    return render(request,'cart/cart_checkout.html',context)