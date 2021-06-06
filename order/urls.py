from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name="addtoshopcart"),
    path('shopcart/', views.shopcart, name="shopcart"),
    path('orderproduct/', views.orderProduct, name="orderproduct"),
    path('deletecartitem/<int:id>', views.deletecartitem, name="deletecartitem"),

]
