from django.shortcuts import render
from .models import Order, OrderItem, Payment, Location
from cart.models import Cart
from esewa.payment import EsewaPayment
from esewa.signature import verify_signature
from django.contrib import messages
import uuid
import base64


# Create your views here.
# For delivery Site.
def delivery_dashboard(request):
    return render(request,'delivery/delivery_dashboard.html')

def pickup(request):
    return render(request,'delivery/pickup.html')

def drop(request):
    return render(request,'delivery/drop.html')

def evidence(request):
    return render(request,'delivery/evidence.html')

def orderhistory(request):
    return render(request,'user/orderhistory.html')

def all_order_history(request):
    return render(request,'user/all_order_history.html')

def order_track(request):
    return render(request,'user/order_track.html')

def confirm_order(request):
    # Extract data from the Post request
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

def success(request,id):
    data = request.GET.get('data')
    is_valid, response = verify_signature(data)
    if is_valid:
        payment = Payment.objects.get(id=id)
        payment.status = 'C'
        payment.save()
        return render(request,'order/success.html')
    else:
        return render(request,'order/failure.html')


def failure(request,id):
    messages.warning(request, 'Payment Failed. If any money was deducted, it will be refunded. Or try contacting Support.')
    return render(request,'order/failure.html')

