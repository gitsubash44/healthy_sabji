from django.urls import path
from . import views

urlpatterns = [
    # path for Users Dashboard
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('product/',views.product,name="product"),
    path('product/<int:id>/',views.productDetail,name="productDetail"),
    path('contact/',views.contact,name="contact"),
    path('upload_photo/',views.upload_photo,name="upload_photo"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('profile/change_password/',views.change_password,name="change_password"),
    path('profile/update',views.user_info_change,name="update_profile"),
    path('search/',views.search,name="search"),
]