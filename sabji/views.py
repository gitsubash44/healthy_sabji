from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import * 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from orders.models import Order
from cart.models import Cart
from django.contrib.auth import update_session_auth_hash 
from django.core import serializers

# For Admin Dashboard
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def user_manage(request):
    return render(request,'admin/user_manage.html')

# For User views Site.
def search(request):
    query = request.GET.get('query')
    products = {}
    if query:
        products = Product.objects.filter(name__icontains=query)
    return render(request, 'user/search.html', {'products': products})


def index(request):
    return render(request, 'user/index.html',)


def about(request):
    return render(request,'user/about.html')

def product(request):
    products = Product.objects.all()
    for product in products:
        if product.quantity == 0:
            product.out_of_stock = True
        else:
            product.out_of_stock = False
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

@login_required
def upload_photo(request):
    if request.method == 'POST':
        user = request.user
        user.photo = request.FILES.get('photo')
        user.save()
        messages.success(request,'Profile Picture Updated Successfully')
        return redirect('user_profile')

@login_required
def user_profile(request):
    password_change_form = PasswordChangeForm(request.user)
    tmp1 = Order.objects.filter(user=request.user,status='P')
    tmp2 = Order.objects.filter(user=request.user,status='OD')
    current_orders = tmp1.union(tmp2)[:3]
    order_history = Order.objects.filter(user=request.user)
    context = {
        'password_change_form':password_change_form,
        'current_orders':current_orders,
        'order_history':order_history
        }
    return render(request,'user/user_profile.html',context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ✅ Prevents logout after password change
            messages.success(request, 'Password changed successfully')
            print("Password changed successfully")
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, error, extra_tags='danger')

    return redirect('user_profile')  # ✅ Redirects back to profile

def user_info_change(request):
    if request.method == 'POST':
        user = request.user
        user.first_name , user.last_name = request.POST.get('name').split()
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request,'User Info Updated Successfully')
        return redirect('user_profile')