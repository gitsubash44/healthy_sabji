from django.shortcuts import render

# Create your views here.

# for Farmer site.
def farmer_dashboard(request):
    return render(request,'farmer/farmer_dashboard.html')

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