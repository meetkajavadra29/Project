from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.home,name='home'),
    path('Registration',views.Registration,name='Registration'),
    path('loginuser',views.loginuser,name='loginuser'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('forgotpass',views.forgotpass,name='forgotpass'),
    path('about',views.about,name='about'),
    path('cart/<int:product_id>/',views.cart,name='cart'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('decrease/<int:product_id>/',views.decrease,name='decrease'),
    path('increase/<int:product_id>/',views.increase,name='increase'),
    path('remove/<int:product_id>/',views.remove,name='remove'),
    path('buynow',views.buynow,name='buynow'),
    path('palce_order',views.palce_order,name='palce_order'),
    path('order',views.order,name='order'),
    path('product_details',views.product_details,name='product_details'),
    path('order_details',views.order_details,name='order_details'),
    path('feedback/<int:product_id>/',views.feedback,name='feedback'),
    path('edit_feedback/<int:product_id>/',views.edit_feedback,name='edit_feedback'),
    path('order_succes',views.order_succes,name='order_succes')

]
