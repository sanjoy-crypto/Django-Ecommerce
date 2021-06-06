from django.urls import path

from . import views
from user import views as UserViews

urlpatterns = [
    path('login/', UserViews.loginPage, name="login"),
    path('signup/', UserViews.signupPage, name="signup"),
    path('logout/', UserViews.logoutPage, name="logout"),
    path('faq/', views.faqPage, name="faq"),

    path('', views.homePage, name="home"),
    path('aboutus/', views.aboutUs, name="aboutus"),
    path('contact/', views.contactUs, name="contact"),
    path('search/', views.search, name="search"),
    path('category/<int:id>/<slug:slug>/',
         views.categoryProduct, name="category_product"),
    path('product/<int:id>/<slug:slug>/',
         views.product_details, name="product_details"),
    path('ajaxcolor/', views.ajaxcolor, name="ajaxcolor"),
]
