from django.shortcuts import render, redirect
from .models import Order, OrderItem, Payment, Location
from cart.models import Cart
from esewa.payment import EsewaPayment
from esewa.signature import verify_signature
from django.contrib import messages
import uuid
import base64
import datetime as dt
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


# Create your views here.
# For delivery Site.
def delivery_dashboard(request):
    if request.user.is_delivery_person != True:
        raise PermissionDenied
    orders = Order.objects.filter(status='OD',delivery_person=request.user)
    all_orders = Order.objects.filter(delivery_person=request.user)
    context = {
        'orders':orders,
        'all_orders':all_orders,
        }
    return render(request,'delivery/delivery_dashboard.html',context)

def pickup(request):
    return render(request,'delivery/pickup.html')

def drop(request):
    orders = Order.objects.filter(status='OD',delivery_person=request.user)
    context = {
        'orders':orders
        }
    return render(request,'delivery/drop.html', context)

@login_required
def evidence(request,order_id):
    if request.method == "POST":
        image = request.FILES.get('evidence')
        order = Order.objects.get(id=order_id)
        order.evidence = image
        order.status = 'D'
        order.save()
        return redirect('delivery_dashboard')
    return redirect('delivery_dashboard')

@login_required
def cancel_order(request,order_id):
    # Comment this
    # if dt.datetime.now().hour >= 12:
    #     messages.warning(request, f'Sorry, Orders can only cancelled before 12 PM.,current time is {dt.datetime.now().hour}:{dt.datetime.now().minute}')
    #     return redirect('product')
    

    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('delivery_dashboard')

@login_required
def evidences(request):
    orders = Order.objects.filter(status='D',delivery_person=request.user)
    context = {
        'orders':orders
        }
    return render(request,'delivery/evidence.html',context)

def orderhistory(request,id):
    order = Order.objects.get(id=id)
    return render(request,'user/orderhistory.html', {'order':order})

def all_order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders
        }
    return render(request,'user/all_order_history.html', context)

def order_track(request,order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order':order,
        }
    return render(request,'user/order_track.html', context)

def confirm_order(request):
    # Extract data from the Post request
    # if dt.datetime.now().hour >= 10:
    #     messages.warning(request, f'Sorry, Orders are only accepted before 10 AM.,current time is {dt.datetime.now().hour}:{dt.datetime.now().minute}')
    #     return redirect('product')
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        house_number_street_name = request.POST.get('house_number_street_name')
        city_area = request.POST.get('city_area')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        order_notes = request.POST.get('order_notes')

        #Create location for dropoff first since it is a foreign key in Order
        location = Location.objects.create(
            first_name=first_name, last_name=last_name,
            address=address, house_number_street_name=house_number_street_name,
            city_area=city_area, mobile=mobile,
            email=email, order_notes=order_notes)

        #Create pending payment for the order since it is a foreign key in Order
        payment_uuid = uuid.uuid4()
        carts = Cart.objects.filter(user=request.user)
        total = 0
        for cart in carts:
            total += cart.product.price * cart.quantity
        
        payment = Payment.objects.create(
            amount=total, payment_method='ESEWA',
            payment_uuid=payment_uuid, status='P')
        
        #Create the pending order with the created location and order
        order = Order.objects.create(
            user=request.user, location=location,
            status='P', payment=payment)
        
        for product in carts:
            OrderItem.objects.create(
                order=order, product=product.product,
                quantity=product.quantity, price=product.product.price)

        epayment = EsewaPayment(
        success_url=f"http://localhost:8000/success/{payment.id}",
        failure_url=f"http://localhost:8000/failure/{payment.id}",

        )
        signature = epayment.create_signature(
            payment.amount,
            payment.payment_uuid
        )
        payment.signature = signature
        payment.save()
        context = {'order': order,'location':location,'payment':payment,'form':epayment.generate_form()}
        return render(request,'order/confirm_order.html',context)

# def success(request,id):
#     data = request.GET.get('data')
#     payment = Payment.objects.get(id=id)
#     epayment = EsewaPayment(
#         success_url=f"http://localhost:8000/success/{payment.id}",
#         failure_url=f"http://localhost:8000/failure/{payment.id}",

#         )
#     epayment.create_signature(
#             payment.amount,
#             payment.payment_uuid
#         )
#     if epayment.is_completed(True):
#         payment.status = 'C'
#         payment.save()
#         return render(request,'order/success.html')
#     else:
        
#         return render(request,'order/failure.html')
@login_required
def success(request,id):
    carts = Cart.objects.filter(user=request.user,active=True)
    for cart in carts:
        cart.active = False
        cart.save()
    data = request.GET.get('data')
    is_valid, response = verify_signature(data)
    if is_valid:
        payment = Payment.objects.get(id=id)
        payment.status = 'C'
        payment.save()
        return render(request,'order/success.html')
    else:
        return render(request,'order/failure.html')

@login_required
def failure(request,id):
    messages.warning(request, 'Payment Failed. If any money was deducted, it will be refunded. Or try contacting Support.')
    return render(request,'order/failure.html')

