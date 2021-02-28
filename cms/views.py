from django import forms
from django.contrib.messages.api import success
from django.db import models
from django.http import request
from cms.models import Customer, Order, Product
from django.shortcuts import render, redirect
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import fields, inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages = success(request, 'user created successfully  ' + username)
            return redirect('login')
        else:
            print(form.is_valid)
    context = {
        'form': form,
    }
    return render(request, 'cms/register.html', context)

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid username or password')
    return render(request, 'cms/login.html')

def logoutUser(request):
    logout(request)
    return render(request, 'cms/login.html')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders= orders.count()
    delivered = orders.filter(status='delivered').count()
    pending_orders = orders.filter(status='pending').count()


    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers, 
        'total_orders': total_orders,
        'delivered': delivered,
        'pending_orders': pending_orders
    }
    return render(request, 'cms/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'cms/product.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders.count(),
        'myfilter': myfilter
        }

    return render(request, 'cms/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=5)
    # form = OrderForm(initial={'customer': customer})
    # remove existing order by using queryset
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    context= {
        'formset': formset,
        }

    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
        else:
            print('invalid form')
    else:
        return render(request, 'cms/orderform.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def OrderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    formset = OrderForm(instance=order)
    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('home')
        else:
            print('invalid form')
    context= {'formset': formset}
    return render(request, 'cms/orderform.html', context)
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def OrderDelete(request, pk):
    order = Order.objects.get(id=pk)
    context = { 'order': order}
    if request.method == "POST":
        order.delete()
        return redirect('home')
    return render(request, 'cms/orderdelete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    print(orders)
    total_orders= orders.count()
    delivered = orders.filter(status='delivered').count()
    pending_orders = orders.filter(status='pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending_orders': pending_orders
    }
    return render(request, 'cms/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form': form
    }
    return render(request, 'cms/account_settings.html', context)