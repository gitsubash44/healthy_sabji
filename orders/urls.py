from django.urls import path
from . import views

urlpatterns = [
    # Path for Delivery Dashboard
    path('delivery_dashboard/',views.delivery_dashboard,name="delivery_dashboard"),
    path('pickup/',views.pickup,name="pickup"),
    path('drop/',views.drop,name="drop"),
    path('evidence/',views.evidence,name="evidence"),
]
