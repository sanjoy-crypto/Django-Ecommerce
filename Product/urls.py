from django.urls import path

from . import views

urlpatterns = [
    path('', views.productPage, name="product"),
    path('addcomment/<int:id>', views.addcomment, name="addcomment"),

]
