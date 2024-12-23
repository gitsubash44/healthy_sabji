from django.shortcuts import render

# For User views Site.
def index(request):
    return render(request, 'user/index.html')


def about(request):
    return render(request,'user/about.html')

def product(request):
    return render(request, 'user/product.html')


def productDetail(request):
    return render(request,'user/product_desc.html')

def cart(request):
    return render(request,'user/cart.html')

def checkout(request):
    return render(request,'user/checkout.html')

def contact(request):
    return render(request,'user/contact.html')

def user_profile(request):
    return render(request,'user/user_profile.html')

def orderhistory(request):
    return render(request,'user/orderhistory.html')

def all_order_history(request):
    return render(request,'user/all_order_history.html')

def order_track(request):
    return render(request,'user/order_track.html')


# For delivery Site.
def delivery_dashboard(request):
    return render(request,'delivery/delivery_dashboard.html')

def pickup(request):
    return render(request,'delivery/pickup.html')

# for Farmer site.
def farmer_dashboard(request):
    return render(request,'farmer/farmer_dashboard.html')