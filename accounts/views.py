from django.shortcuts import render, redirect
from sabji.models import Product,Category
from orders.models import Order
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


# For Users authentication
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.is_farmer:
                return redirect('farmer_dashboard')  # Redirect farmers
            elif user.is_delivery_person:
                return redirect('delivery_dashboard')  # Redirect delivery personnel
            else:
                return redirect('index')  # Redirect regular users
        
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

    return render(request, 'account/login.html')


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
@login_required
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

@login_required
def farmer_profile(request):
    return render(request,'farmer/farmer_profile.html')

@login_required
def add_products(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        product = Product(
            name = name,
            price = price,
            description = description,
            image = image,
            quantity = quantity,
            category = Category.objects.get(id=category)
        )
        product.save()
        messages.success(request,'Product added successfully')
        return redirect('farmer_dashboard')
    return render(request,'farmer/add_products.html')

@login_required
def edit_product(request,id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.quantity = request.POST.get('quantity')
        product.category = Category.objects.get(id=request.POST.get('category'))
        product.save()
        messages.success(request,'Product updated successfully')
        return redirect('farmer_dashboard')
    context = {
        'product':product
    }
    return render(request,'farmer/add_products.html',context)


def farmer_products(request):
    return render(request,'farmer/farmer_products.html')

@login_required
def new_order(request):
    orders = Order.objects.filter(status='P')
    deliverers = CustomUser.objects.filter(is_delivery_person=True)
    for order in orders:
        total = 0
        for item in order.items.all():
            total += item.quantity
        order.total = total
    context = {
        'orders':orders,
        'deliverers':deliverers
    }
    return render(request,'farmer/new_order.html',context)

@login_required
def drop_delivery(request):
    orders = Order.objects.filter(status='OD')
    for order in orders:
        total = 0
        for item in order.items.all():
            total += item.quantity
        order.total = total
    context = {
        'orders':orders
    }
    return render(request,'farmer/drop_delivery.html',context)

@login_required
def assign_deliverer(request,id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        order.delivery_person = CustomUser.objects.get(id=request.POST.get('deliverer'))
        order.status = 'OD'
        order.save()
        messages.success(request,'Order assigned to deliverer')
        return redirect('new_order')
