from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from Product.models import *
from .forms import SearchForm
import json
from order.models import *

# Create your views here.


def homePage(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    slider_image = SliderImage.objects.all().order_by('id')[:3]
    offer_image = OfferImage.objects.all().order_by('id')[:3]
    latest_product = Product.objects.all().order_by('-id')[:10]
    featured_product = Product.objects.all().order_by('?')[:10]
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity
    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    # page = "Home"

    context = {'setting': setting,
               'category': category, 'slider_image': slider_image, 'total': total, 'offer_image': offer_image, 'latest_product': latest_product, 'featured_product': featured_product, 'cartitems': cartitems}
    return render(request, 'Home/home.html', context)


def aboutUs(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    context = {'setting': setting,
               'category': category, 'cartitems': cartitems, 'total': total}
    return render(request, 'Home/about.html', context)


def contactUs(request):
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity
    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

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

    context = {'setting': setting, 'form': form,
               'category': category, 'cartitems': cartitems, 'total': total}
    return render(request, 'Home/contact.html', context)


def categoryProduct(request, id, slug):
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    setting = Setting.objects.get(id=1)
    context = {'products': products, 'category': category,
               'setting': setting, 'cartitems': cartitems, 'total': total}
    return render(request, 'Home/category_product.html', context)


def search(request):
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
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
                       'category': category, 'query': query, 'setting': setting, 'cartitems': cartitems, 'total': total}
            return render(request, 'Home/searchProduct.html', context)
    return HttpResponseRedirect('/')


def product_details(request, id, slug):
    query = request.GET.get('q')
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    featured_product = Product.objects.all().order_by('?')[:10]
    comments = Comment.objects.filter(product_id=id, status='True')

    context = {'product': product, 'category': category,
               'images': images, 'comments': comments, 'featured_product': featured_product, 'setting': setting, 'cartitems': cartitems, 'total': total}

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            # selected product by click color radio
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(
                product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:' + \
                str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(
                product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                       'variant': variant, 'query': query})

    return render(request, 'Home/productDetails.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string(
            'color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def faqPage(request):
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()

    faq = FAQ.objects.filter(status="True").order_by('ordernumber')

    context = {
        'faq': faq, 'category': category, 'setting': setting, 'cartitems': cartitems, 'total': total
    }
    return render(request, 'Home/faq.html', context)
