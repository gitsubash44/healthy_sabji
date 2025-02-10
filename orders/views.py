from django.shortcuts import render

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

