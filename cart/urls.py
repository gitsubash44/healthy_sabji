from django.urls import path
from . import views


urlpatterns = [
    path('cart/add/<int:id>/<int:quantity>/', views.add_to_cart, name="add_to_cart"),
    path('cart/add/<int:id>/', views.increase_cart, name="increase_cart"),
    path('cart/remove/<int:id>/', views.decrease_cart, name="decrease_cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
]