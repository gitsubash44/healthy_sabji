"""
URL configuration for healthy_sabji project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sabji import views

urlpatterns = [
    # path for Users Dashboard
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('product/',views.product,name="product"),
    path('product_desc/',views.productDetail,name="productDetail"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name="contact"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('orderhistory/',views.orderhistory,name="orderhistory"),
    path('all_order_history/',views.all_order_history,name="all_order_history"),
    path('order_track/',views.order_track,name="order_track"),
    
    # Path for Delivery Dashboard
    path('delivery_dashboard/',views.delivery_dashboard,name="delivery_dashboard"),
    path('pickup/',views.pickup,name="pickup"),
    path('drop/',views.drop,name="drop"),
    path('evidence/',views.evidence,name="evidence"),
    
    #Path for Farmer Dashboard
    path('farmer_dashboard/',views.farmer_dashboard,name="farmer_dashboard"),
    path('farmer_profile/',views.farmer_profile,name="farmer_profile"),
]
