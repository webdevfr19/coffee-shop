from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, Http404
import json
from .models import Product, Cart, OrderItem, Customer
# from .forms import ProductForm
# Create your views here.

def Error404(request):
    return render(request, 'base/404.html')

def home(request):
    featured_products = Product.objects.all()[:3]
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'base/main.html', context)

def Userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    context = {

    }
    return render(request, 'base/login.html', context)

# def UserLogout(request):
#     logout(request)
#     return redirect('home')

def Usersignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('customer-info')
    else:
        return render(request, 'base/signup.html')

def customerInfo(request):
    current_user = request.user
    if request.method == 'POST':
        user = current_user
        name = current_user
        email = current_user.email
        address = request.POST['address']
        city = request.POST['city']
        customer = Customer.objects.create(email=email, name=name, user=user, address=address, city=city)
        return redirect('login')
    else:
        return render(request, 'base/customer-info.html')

@login_required(login_url='login')
def userProfile(request, pk):
    current_user = request.user
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return redirect('error404')
    if request.method == 'POST':
        customer.name = request.POST.get('username')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.city = request.POST.get('city')
        customer.save()
        return redirect('home')
    else:
        context = {
            'customer': customer,
        }
        return render(request, 'base/user-settings.html', context)

def menu(request):
    drink_products = Product.objects.filter(category=1)
    food_products = Product.objects.filter(category=4) # i dont know what happened with database but its working lol
    merch_products = Product.objects.filter(category=5)
    context = {
        'food_products': food_products,
        'drink_products': drink_products,
        'merch_products': merch_products,
    }
    return render(request, 'base/menu.html', context)

@login_required(login_url='login')
def orderDrink(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return redirect('error404')
    context = {
        'product': product,
    }
    return render(request, 'base/drink_item.html', context)

@login_required(login_url='login')
def orderFood(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return redirect('error404')
    context = {
        'product': product,
    }
    return render(request, 'base/food_item.html', context)

@login_required(login_url='login')
def orderMerch(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return redirect('error404')
    context = {
        'product': product,
    }
    return render(request, 'base/merch_item.html', context)

@login_required(login_url='login')
def addCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart = Cart.objects.get_or_create(user=request.user, products=product, total_price=product.price)
    cart.save()
    return redirect('menu')

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'base/cart.html', context)

@login_required(login_url='login')
def delivery(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'base/delivery.html', context)

@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Cart.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added in the cart', safe=False)