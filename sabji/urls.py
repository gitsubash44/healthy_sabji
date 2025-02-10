from django.urls import path
from . import views

urlpatterns = [
    # path for Users authentication
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    
    # path for Users Dashboard
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('product/',views.product,name="product"),
    path('product/<int:id>/',views.productDetail,name="productDetail"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name="contact"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('orderhistory/',views.orderhistory,name="orderhistory"),
    path('all_order_history/',views.all_order_history,name="all_order_history"),
    path('order_track/',views.order_track,name="order_track"),
]