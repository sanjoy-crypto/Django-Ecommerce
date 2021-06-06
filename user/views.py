from django.shortcuts import render, redirect
from django.http import HttpResponse
from Home.models import *
from Product.models import *
from order.models import *
from .models import *
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.


@login_required(login_url='/login')  # Check login
def index(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'setting': setting,
               'category': category, 'cartitems': cartitems, 'total': total,
               'profile': profile}
    return render(request, 'Home/user_profile.html', context)


def loginPage(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is Incorrect')

    context = {'setting': setting,
               'category': category, 'cartitems': cartitems, 'total': total}
    return render(request, 'Home/login_page.html', context)


def signupPage(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created')
            return redirect('/')
        else:
            messages.warning(request, form.errors)
            return redirect('/signup')

    form = SignUpForm()

    context = {'setting': setting,
               'category': category, 'cartitems': cartitems, 'total': total, 'form': form}
    return render(request, 'Home/signup_page.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')  # Check login
def user_update(request):
    setting = Setting.objects.get(id=1)
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form, 'setting': setting,
        }
        return render(request, 'Home/user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/user')
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'Home/user_password.html', {'form': form, 'setting': setting, 'category': category})


@login_required(login_url='/login')  # Check login
def user_orders(request):

    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    current_user = request.user

    orders = Order.objects.filter(user_id=current_user.id)

    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity
    context = {'category': category,
               'orders': orders,
               'setting': setting, 'cartitems': cartitems, 'total': total
               }
    return render(request, 'Home/user_orders.html', context)


def order_detail(request, id):
    setting = Setting.objects.get(id=1)
    shopcart = ShopCart.objects.all()
    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'setting': setting,
        'category': category, 'cartitems': cartitems, 'total': total,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'Home/user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    setting = Setting.objects.get(id=1)
    shopcart = ShopCart.objects.all()
    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(
        user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'order_product': order_product,
               'total': total,
               'cartitems': cartitems,
               'setting': setting,
               }
    return render(request, 'Home/user_order_products.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product_detail(request, id, oid):
    setting = Setting.objects.get(id=1)
    shopcart = ShopCart.objects.all()
    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'total': total,
        'cartitems': cartitems,
        'setting': setting,
    }
    return render(request, 'Home/user_order_detail.html', context)


@login_required(login_url='/login')
def user_comments(request):

    setting = Setting.objects.get(id=1)
    shopcart = ShopCart.objects.all()
    total = 0
    for prod in shopcart:
        total += prod.product.price * prod.quantity

    cartitems = 0
    for item in shopcart:
        cartitems += item.quantity

    category = Category.objects.all()

    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'total': total,
        'cartitems': cartitems,
        'setting': setting,
        'comments': comments,
    }
    return render(request, 'Home/user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return redirect('/user/comments')
