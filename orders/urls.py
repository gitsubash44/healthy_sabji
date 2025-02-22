from django.urls import path
from . import views

urlpatterns = [
    path('confirm_order/',views.confirm_order,name="confirm_order"),
    path('delivery_dashboard/',views.delivery_dashboard,name="delivery_dashboard"),
    path('drop/',views.drop,name="drop"),
    path('evidence/<int:order_id>/',views.evidence,name="evidence"),
    path('evidences/',views.evidences,name="evidences"),    
    path('orderhistory/',views.orderhistory,name="orderhistory"),
    path('all_order_history/',views.all_order_history,name="all_order_history"),
    path('order_track/',views.order_track,name="order_track"),
    path('success/<int:id>',views.success,name="success"),
    path('failure/<int:id>',views.failure,name="failure"),
]
