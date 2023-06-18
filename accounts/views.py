from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .filters import Orderfilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
#from .decorators import unauthenticated_user, allowed_us, admin_only
from .decorators import unauthenticated_user,admin_only,allowed_us


@login_required(login_url='login')
@allowed_us(allowed_user=['customer'])
def accountsettings(request):
    customer=request.user.customer
    form=Customerform(instance=customer)

    if request.method=='POST':
        form=Customerform(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()


    context={
        'form':form,
    }
    return render(request,'accounts/account_settings.html',context)


@login_required(login_url='login')
@allowed_us(allowed_user=['customer'])
def userpage(request):
    orders=request.user.customer.order_set.all()

    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={
        "orders":orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,

    }
    return render(request,'accounts/user.html',context)



def register(request):
    form=Createuserform()
    if request.method=="POST":
        form=Createuserform(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            
            messages.success(request,'Account was created for' + username)
            return redirect("login")
    context={
        "form":form,
        
    }
    return render(request,'accounts/register.html',context)



@unauthenticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user_page')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    context={

    }
    return render(request, "accounts/login.html",context)

def logoutuser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()

    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={
        "customers":customers,
        "orders":orders,
        "total_customers":total_customers,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending,
    }
    return render(request,'accounts/dashboard.html',context)



@login_required(login_url='login')
@allowed_us(allowed_user=['admin'])
def products(request):
    products=Product.objects.all()
    context={
        "products":products,
    }
    return render(request,"accounts/products.html",context)



@login_required(login_url='login')
@allowed_us(allowed_user=['admin'])
def customers(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    myfilter=Orderfilter(request.GET,queryset=orders)
    orders=myfilter.qs
    context={
        "customer":customer,
        "orders":orders,
        "order_count":order_count,
        "myfilter":myfilter,
    }

    return render(request,'accounts/customer.html',context)



@login_required(login_url='login')
@allowed_us(allowed_user=['admin'])
def createOrder(request,pk):
    orderformset=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset=orderformset(queryset=Order.objects.none(), instance=customer)
    #form = Orderform(initial={'customer': customer})
    if request.method=="POST":
        #form=Orderform(request.POST,)
        formset=orderformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        

    context={
        "formset":formset,
    }
    return render(request, 'accounts/order_form.html',context)



@login_required(login_url='login')
@allowed_us(allowed_user=['admin'])
def Updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form=Orderform(instance=order)
    if request.method=="POST":
        form=Orderform(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context={
        "form":form,
    }

    return render(request,'accounts/update_order.html',context)



@login_required(login_url='login')
@allowed_us(allowed_user=['admin'])
def Delete(request,pk):
    order=Order.objects.get(id=pk)
    
    if request.method=="POST":
        order.delete()
        return redirect("/")
        
    context={
        "item":order,
    }
    return render(request,'accounts/delete.html',context)