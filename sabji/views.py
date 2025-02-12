from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import * 
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

# For Admin Dashboard
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def user_manage(request):
    return render(request,'admin/user_manage.html')

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

# For User views Site.
def index(request):
    return render(request, 'user/index.html')


def about(request):
    return render(request,'user/about.html')

def product(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'user/product.html', {'products': products})


def productDetail(request,id):
    product = Product.objects.get(id=id)
    return render(request,'user/product_desc.html',{'product':product})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name,email=email,message=message)
        contact.save()
        messages.success(request,'Your message has been sent successfully')
        return redirect('contact')
    return render(request,'user/contact.html')

def user_profile(request):
    return render(request,'user/user_profile.html')
