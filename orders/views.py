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


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.
# For delivery Site.
@login_required
def delivery_dashboard(request):
    if request.user.is_delivery_person != True:
        raise PermissionDenied
    orders = Order.objects.filter(status='OD', delivery_person=request.user)
    all_orders = Order.objects.filter(delivery_person=request.user)
    for order in orders:
        order.delivery_address = {
            'last_name': order.location.last_name,
            'first_name': order.location.first_name,
            'address': order.location.address,
            'house_number_street_name': order.location.house_number_street_name,
            'city_area': order.location.city_area,
            'mobile': order.location.mobile,
            'email': order.location.email,
        }
        order.pickup_addresses = []
        for item in order.items.all():
            farmer_location = item.product.farmer.address if item.product.farmer else 'No pickup location available'
            order.pickup_addresses.append({
                'product_name': item.product.name,
                'farmer_name': item.product.farmer.username if item.product.farmer else 'Unknown Farmer',
                'pickup_address': farmer_location
            })
            
    context = {
        'orders': orders,
        'all_orders': all_orders,
    }
    return render(request, 'delivery/delivery_dashboard.html', context)


def pickup(request):
    return render(request,'delivery/pickup.html')

@login_required
def drop(request):
    orders = Order.objects.filter(status='OD',delivery_person=request.user)
    for order in orders:
        order.delivery_address = {
            'last_name': order.location.last_name,
            'first_name': order.location.first_name,
            'address': order.location.address,
            'house_number_street_name': order.location.house_number_street_name,
            'city_area': order.location.city_area,
            'mobile': order.location.mobile,
            'email': order.location.email,
        }
        
        order.pickup_addresses = []
        for item in order.items.all():
            farmer_location = item.product.farmer.address if item.product.farmer else 'No pickup location available'
            order.pickup_addresses.append({
                'product_name': item.product.name,
                'farmer_name': item.product.farmer.username if item.product.farmer else 'Unknown Farmer',
                'pickup_address': farmer_location,
                'farmer_phone': item.product.farmer.phone_number if item.product.farmer else 'Unknown Farmer Phone',
            })
    context = {
        'orders': orders
    }
    return render(request, 'delivery/drop.html', context)

@login_required
def evidence(request,order_id):
    if request.method == "POST":
        print(request.FILES)
        image = request.FILES.get('evidence')
        order = Order.objects.get(id=order_id)
        print(order,order_id)
        order.evidence = image
        order.status = 'D'
        order.save()
        return redirect('delivery_dashboard')
    return redirect('delivery_dashboard')

@login_required
def cancel_order(request, order_id):
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
        method = request.POST.get('method')
        if method == 'COD':
            return pay_via_cod(request)

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
    
def pay_via_cod(request):
    paymentobj = Payment.objects.create(
        amount=0, payment_method='COD',
        signature = "Cash On Delivery",
        payment_uuid=uuid.uuid4(), status='C')
    order = Order.objects.create(
        user=request.user, location=None,
        status='C', payment=paymentobj)
    carts = Cart.objects.filter(user=request.user)
    for product in carts:
        OrderItem.objects.create(
            order=order, product=product.product,
            quantity=product.quantity, price=product.product.price)
    for cart in carts:
        cart.active = False
        cart.save()
    order_items = order.items.all()
    return render(request,'order/success.html',{'transaction_id':paymentobj.payment_uuid,'order_items':order_items})


@login_required
def success(request,id):
    carts = Cart.objects.filter(user=request.user,active=True)
    for cart in carts:
        cart.active = False
        cart.save()
    data = request.GET.get('data')
    payment = Payment.objects.get(id=id)
    epayment = EsewaPayment(
        success_url=f"http://localhost:8000/success/{payment.id}",
        failure_url=f"http://localhost:8000/failure/{payment.id}",
        )
    signature = epayment.create_signature(
            payment.amount,
            payment.payment_uuid
        )
    is_valid = epayment.is_completed(True)
    if is_valid:
        payment.status = 'C'
        payment.save()
        # Get the order associated with this payment
        order = Order.objects.filter(payment=payment).first()
        if order:
            order_items = order.items.all()
            for item in order_items:
                product = item.product
                product.decrease_quantity(item.quantity)
        
        return render(request,'order/success.html',{'transaction_id':payment.payment_uuid,'order_items':order_items})
    else:
        return render(request,'order/failure.html')

@login_required
def failure(request,id):
    messages.warning(request, 'Payment Failed. If any money was deducted, it will be refunded. Or try contacting Support.')
    return render(request,'order/failure.html')



# Generate PDF Invoice
# This function generates a PDF invoice for the order and returns it as a response.
def generate_invoice(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
        
        pdf = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Header
        title = Paragraph("<b style='font-size:18px; color:green;'>Healthy Sabji - Invoice</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Order Details
        order_details = [
            ["Order ID:", str(order.id)],
            ["Customer:", order.user.email if order.user else "N/A"],
            ["Order Date:", order.order_date.strftime('%Y-%m-%d') if order.order_date else "N/A"],
            ["Status:", order.get_status_display() if order.status else "N/A"],
        ]
        
        if order.location:
            address = order.location.address if order.location.address else ""
            city_area = order.location.city_area if order.location.city_area else ""
            order_details.append(["Delivery Address:", f"{address}, {city_area}"])

        details_table = Table(order_details, colWidths=[120, 300])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 12))

        # Order Items
        order_items = [["Product", "Quantity", "Unit Price", "Total Price"]]
        total_price = 0

        for item in order.items.all():
            if item.product:  # Check if product exists
                total = item.quantity * item.product.price
                order_items.append([
                    item.product.name,
                    str(item.quantity),
                    f"{item.product.price:.2f}",
                    f"{total:.2f}"
                ])
                total_price += total

        order_items.append(["", "", "Total Amount:", f"${total_price:.2f}"])

        items_table = Table(order_items, colWidths=[200, 80, 100, 100])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(items_table)

        # Payment Info
        if hasattr(order, 'payment') and order.payment:
            payment_info = [
                ["Payment Status:", order.payment.get_status_display() if order.payment.status else "N/A"],
                ["Payment Method:", order.payment.payment_method if order.payment.payment_method else "N/A"],
                ["Payment ID:", str(order.payment.payment_uuid) if order.payment.payment_uuid else "N/A"],
            ]
            payment_table = Table(payment_info, colWidths=[150, 300])
            payment_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(Spacer(1, 12))
            elements.append(payment_table)

        # Footer
        thank_you = Paragraph("<b style='font-size:14px; color:darkgreen;'>Thank you for shopping with Healthy Sabji!</b>", styles["Normal"])
        elements.append(Spacer(1, 20))
        elements.append(thank_you)

        pdf.build(elements)
        return response

    except Exception as e:
        return HttpResponse(f"Error generating invoice: {str(e)}", status=500)