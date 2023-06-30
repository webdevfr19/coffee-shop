from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Product, Cart, OrderItem, Customer
# from .forms import ProductForm
# Create your views here.

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

def userProfile(request, pk):
    current_user = request.user
    customer = Customer.objects.get(id=pk)
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
    customer = request.user.customer
    order = Cart.objects.get(customer=customer)
    drink_products = Product.objects.filter(category=1)
    food_products = Product.objects.filter(category=4) # i dont know what happened with database but its working lol
    merch_products = Product.objects.filter(category=5)
    cartItems = order.get_cart_items
    context = {
        'food_products': food_products,
        'drink_products': drink_products,
        'merch_products': merch_products,
        'cartItems': cartItems,
    }
    return render(request, 'base/menu.html', context)

def orderDrink(request, pk):
    product = Product.objects.filter(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'base/drink_item.html', context)

def orderFood(request, pk):
    product = Product.objects.filter(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'base/food_item.html', context)

def orderMerch(request, pk):
    product = Product.objects.filter(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'base/merch_item.html', context)

def addCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart = Cart.objects.get_or_create(user=request.user, products=product, total_price=product.price)
    cart.save()
    return redirect('menu')

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