from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from Product.models import *
from .forms import SearchForm
import json

# Create your views here.


def homePage(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    slider_image = SliderImage.objects.all().order_by('id')[:3]
    offer_image = OfferImage.objects.all().order_by('id')[:3]
    latest_product = Product.objects.all().order_by('-id')[:10]
    featured_product = Product.objects.all().order_by('?')[:10]
    # page = "Home"

    context = {'setting': setting,
               'category': category, 'slider_image': slider_image, 'offer_image': offer_image, 'latest_product': latest_product, 'featured_product': featured_product}
    return render(request, 'Home/home.html', context)


def aboutUs(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()

    context = {'setting': setting, 'category': category}
    return render(request, 'Home/about.html', context)


def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(
                request, 'Your message has been sent. Thank you for your message.')
            return redirect('contact')

    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    form = ContactForm

    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'Home/contact.html', context)


def categoryProduct(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    setting = Setting.objects.get(id=1)
    context = {'products': products, 'category': category, 'setting': setting}
    return render(request, 'Home/category_product.html', context)


def search(request):
    setting = Setting.objects.get(id=1)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catId = form.cleaned_data['catId']
            if catId == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=catId)

            category = Category.objects.all()
            context = {'products': products,
                       'category': category, 'query': query, 'setting': setting}
            return render(request, 'Home/searchProduct.html', context)
    return HttpResponseRedirect('/')


def product_details(request, id, slug):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    featured_product = Product.objects.all().order_by('?')[:10]
    comments = Comment.objects.filter(product_id=id, status='True')

    context = {'product': product, 'category': category,
               'images': images, 'comments': comments, 'featured_product': featured_product, 'setting': setting}

    return render(request, 'Home/productDetails.html', context)
