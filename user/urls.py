from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="user"),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='password'),
    path('orders/', views.user_orders, name='orders'),
    path('orderdetail/<int:id>', views.order_detail, name='orderdetail'),
    path('orders_product/', views.user_order_product, name="user_order_product"),
    path('order_product_detail/<int:id>/<int:oid>',
         views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment,
         name='user_deletecomment'),

]
