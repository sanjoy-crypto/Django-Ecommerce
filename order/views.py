from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Product.models import *
from Home.models import *

from user.models import *
from .models import *
from django.utils.crypto import get_random_string
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

    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    context = {'shopcart': shopcart, 'category': category,
               'setting': setting, 'total': total, 'cartitems': cartitems}

    return render(request, 'Home/shopCart.html', context)


@login_required(login_url='/login')
def deletecartitem(request, id):
    ShopCart.objects.filter(id=id).delete()

    messages.success(request, 'Successfully deleted')
    return HttpResponseRedirect('/order/shopcart')


def orderProduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(id=1)

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity

                detail.price = rs.product.price
                detail.amount = rs.total_amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

                # ************ <> *****************

            # Clear & Delete shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(
                request, "Your Order has been completed. Thank you ")
            return render(request, 'Home/Order_Completed.html', {'ordercode': ordercode, 'total': total, 'cartitems': cartitems, 'category': category, 'setting': setting})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()

    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'form': form,
               'profile': profile,
               'category': category,
               'total': total,
               'cartitems': cartitems,
               'setting': setting,
               }
    return render(request, 'Home/Order_Form.html', context)
