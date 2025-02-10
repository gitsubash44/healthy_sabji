from django.urls import path
from . import views

urlpatterns = [
    #Path for Farmer Dashboard
    path('farmer_dashboard/',views.farmer_dashboard,name="farmer_dashboard"),
    path('farmer_profile/',views.farmer_profile,name="farmer_profile"),
    path('add_products/',views.add_products,name="add_products"),
    path('farmer_products/',views.farmer_products,name="farmer_products"),
    path('new_order/',views.new_order,name="new_order"),
    path('drop_delivery/',views.drop_delivery,name="drop_delivery"),
]