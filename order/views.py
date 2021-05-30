from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Product.models import *
from Home.models import *

# Create your views here.


def index(request):
    return HttpResponse('Order page')


@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Product added to Shopcart')
        return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Product added to Shopcart')
        return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(id=1)

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    context = {'shopcart': shopcart, 'category': category,
               'setting': setting, 'total': total}

    return render(request, 'Home/shopCart.html', context)


@login_required(login_url='/login')
def deletecartitem(request, id):
    ShopCart.objects.filter(id=id).delete()

    messages.success(request, 'Successfully deleted')
    return HttpResponseRedirect('/order/shopcart')
