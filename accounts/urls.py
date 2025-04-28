from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
        # path for Users authentication
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout_view,name="logout"),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('forgot-password/sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    
    #Path for Farmer Dashboard
    path('farmer_dashboard/',views.farmer_dashboard,name="farmer_dashboard"),
    path('farmer_profile/',views.farmer_profile,name="farmer_profile"),
    path('add_products/',views.add_products,name="add_products"),
    path('edit_product/<int:id>/',views.edit_product,name="edit_product"),
    path('delete_product/<int:id>/',views.delete_product,name="delete_product"),
    path('farmer_products/',views.farmer_products,name="farmer_products"),
    path('new_order/',views.new_order,name="new_order"),
    path('drop_delivery/',views.drop_delivery,name="drop_delivery"),
    path('delivered/',views.delivered,name="delivered"),
    path('assign_delivery/<int:id>/',views.assign_deliverer,name="assign_deliverer"),
]