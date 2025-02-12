from django.shortcuts import render
from sabji.models import Product
from orders.models import Order

# Create your views here.

# for Farmer site.
def farmer_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    total = 0 
    for o in orders:
        total += o.payment.amount
    context = {
        'products':products,
        'orders':orders,
        'total':total
    }
    return render(request,'farmer/farmer_dashboard.html', context)


def farmer_profile(request):
    return render(request,'farmer/farmer_profile.html')

def add_products(request):
    return render(request,'farmer/add_products.html')

def farmer_products(request):
    return render(request,'farmer/farmer_products.html')

def new_order(request):
    return render(request,'farmer/new_order.html')

def drop_delivery(request):
    return render(request,'farmer/drop_delivery.html')