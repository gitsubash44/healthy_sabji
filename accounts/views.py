from django.shortcuts import render, redirect
from sabji.models import Product,Category
from orders.models import Order
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.validation import validate_custom_password

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            next = request.GET.get('next',None)
            if next:
                return redirect(next)
            else:
                if user.is_farmer:
                    return redirect('farmer_dashboard')
                elif user.is_delivery_person:
                    return redirect('delivery_dashboard')
                else:
                    return redirect('index')
        
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
        address = request.POST.get('address')
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
        if len(phone_number)!= 10 or not phone_number.isdigit():
                messages.error(request, "Phone Number must be 10 digits and contain number only")
                return redirect('register')
        # Validate password
        errors = validate_custom_password(password)
        if errors:
            messages.error(request, errors[0])
            return redirect('register')
        if user_type== 'F':
            Farmer = True
        user = CustomUser.objects.create_user(
            username=username.strip(),
            email=email,password=password,phone_number=phone_number,address=address,is_farmer=Farmer)
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
    # Get products for the current farmer (or all products if superuser)
    products = Product.objects.filter(farmer=request.user)
    if request.user.is_superuser:
        products = Product.objects.all()
    
    orders = Order.objects.filter(
        items__product__farmer=request.user
    ).distinct().prefetch_related('items__product', 'payment').order_by('-created_at')  # Order by newest first
    
    for order in orders:
        total_quantity = 0
        for item in order.items.filter(product__farmer=request.user):
            total_quantity += item.quantity
        order.total = total_quantity  # Total quantity for the order
    
    total_income = 0
    for order in orders:
        for item in order.items.filter(product__farmer=request.user):
            total_income += item.product.price * item.quantity   
            
    context = {
        'products': products,
        'orders': orders,
        'total': total_income
    }
    return render(request, 'farmer/farmer_dashboard.html', context)


@login_required
def farmer_profile(request):
    return render(request,'farmer/farmer_profile.html')

@login_required
def add_products(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        non_discount_price = request.POST.get('non_discount_price', None)
        description = request.POST.get('description')
        image = request.FILES.get('image')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        farmer = request.user

        # Validate price and quantity
        if float(price) <= 0:
            messages.error(request, 'Keep price above Zero')
            return redirect('add_products')
        if int(quantity) <= 0:
            messages.error(request, 'Quantity is Zero')
            return redirect('add_products')
        if non_discount_price and float(non_discount_price) < float(price):
            messages.error(request, 'Pre-discount price must be greater than or equal to the price')
            return redirect('add_products')

        product = Product(
            name=name,
            price=price,
            farmer=farmer,
            pre_discount_price=non_discount_price if non_discount_price else None,
            description=description,
            image=image,
            quantity=quantity,
            category=Category.objects.get(id=category)
        )
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('add_products')
    return render(request, 'farmer/add_products.html')


@login_required
def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        non_discount_price = request.POST.get('non_discount_price', None)
        description = request.POST.get('description')
        image = request.FILES.get('image', None)
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')

        # Validate price and quantity
        if float(price) <= 0:
            messages.error(request, 'Keep price above Zero')
            return redirect('edit_product', id=id)
        if int(quantity) <= 0:
            messages.error(request, 'Quantity is Zero')
            return redirect('edit_product', id=id)
        if non_discount_price and float(non_discount_price) < float(price):
            messages.error(request, 'Pre-discount price must be greater than or equal to the price')
            return redirect('edit_product', id=id)

        # Update product fields
        product.name = name
        product.price = price
        product.pre_discount_price = non_discount_price if non_discount_price else None
        product.description = description
        if image:
            product.image = image
        product.quantity = quantity
        product.category = Category.objects.get(id=category)
        product.save()

        messages.success(request, 'Product updated successfully')
        return redirect('add_products')

    context = {
        'product': product
    }
    return render(request, 'farmer/add_products.html', context)

@login_required
def delete_product(request,id):
    if request.method == "POST":
        print(request.user.is_farmer)
        print(request.user.is_superuser)
        if request.user.is_farmer or request.user.is_superuser:
            product = Product.objects.get(id=id)
            if product.farmer == request.user or request.user.is_superuser:
                product.image.delete()
                product.delete()
                messages.success(request,'Product deleted successfully')
            else:
                messages.error(request,'You are not authorized to delete this product',extra_tags='danger')
        else:
            messages.error(request,'You are not authorized to delete this product',extra_tags='danger')
        
    next = request.META['HTTP_REFERER']
    return redirect(next)  


def farmer_products(request):
    products = Product.objects.filter(farmer=request.user)
    return render(request,'farmer/farmer_products.html')

@login_required
def new_order(request):
    orders = Order.objects.filter(
        items__product__farmer=request.user, 
        status='P'
    ).distinct()
    deliverers = CustomUser.objects.filter(is_delivery_person=True)
    for order in orders:
        total = 0
        farmer_ids = set()  # to collect all farmer ids in the order
        for item in order.items.all():
            total += item.quantity
            farmer_ids.add(item.product.farmer_id)  # collect farmer id from each item
        order.total = total
        # homogenous means only 1 unique farmer (and it's the current user)
        order.is_homogenous = (len(farmer_ids) == 1 and request.user.id in farmer_ids)
        
    context = {
        'orders':orders,
        'deliverers':deliverers
    }
    return render(request,'farmer/new_order.html',context)

@login_required
def drop_delivery(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id, items__product__farmer=request.user, status='OD')
            order.status = 'D'  # Update status to Delivered
            order.save()
            messages.success(request, 'Order marked as delivered successfully')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found or you are not authorized to update this order')
        return redirect('drop_delivery')

    orders = Order.objects.filter(
        items__product__farmer=request.user, 
        status='OD'
    ).distinct()
    for order in orders:
        total = 0
        for item in order.items.all():
            total += item.quantity
        order.total = total
    context = {
        'orders': orders
    }
    return render(request, 'farmer/drop_delivery.html', context)

def delivered(request):
    orders = Order.objects.filter(
        items__product__farmer=request.user, 
        status='D'
    ).distinct()
    for order in orders:
        total = 0
        for item in order.items.all():
            total += item.quantity
        order.total = total
    context = {
        'orders': orders
    }
    return render(request, 'farmer/delivered.html', context)

@login_required
def assign_deliverer(request,id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        order.delivery_person = CustomUser.objects.get(id=request.POST.get('deliverer'))
        order.status = 'OD'
        order.save()
        messages.success(request,'Order assigned to deliverer')
        return redirect('new_order')
