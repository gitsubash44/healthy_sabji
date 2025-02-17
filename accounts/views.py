from django.shortcuts import render, redirect
from sabji.models import Product
from orders.models import Order
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponse

# Create your views here.


# For Users authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Username or Password is incorrect')
            return redirect('login')
    return render(request,'account/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        address= request.POST.get('address')
        user_type = request.POST.get('user_type')
        Farmer = False
        if password != password1:
            messages.error(request,'Password does not match')
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('register')
        if user_type== 'F':
            farmer = True
        user = CustomUser.objects.create_user(username=username,email=email,password=password,phone_number=phone_number,address=address,is_farmer=Farmer)
        user.save()
        messages.success(request,'Account created successfully')
        return redirect('login')
    return render(request,'account/register.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return HttpResponse("GET request not allowed",status=405)



# for Farmer site.
def farmer_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.filter(status='P')
    for order in orders:
        total = 0
        for item in order.items.all():
            total += item.quantity
        order.total = total        
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