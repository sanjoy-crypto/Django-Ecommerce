from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('aboutus/', views.aboutUs, name="aboutus"),
    path('contact/', views.contactUs, name="contact"),
    path('search/', views.search, name="search"),
    path('category/<int:id>/<slug:slug>/',
         views.categoryProduct, name="category_product"),
    path('product/<int:id>/<slug:slug>/',
         views.product_details, name="product_details"),
]
