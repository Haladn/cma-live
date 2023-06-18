from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def unauthenticated_user(view_func):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_function
  
def admin_only(func):
    def wrapper(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='admin':
            return func(request,*args,**kwargs)
        if group=='customer':
            return redirect('login')
        else:
            return redirect('register')
    return wrapper

def allowed_us(allowed_user=[]):
    def decorator(func):
        def wrapper(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_user:    
                return func(request,*args,**kwargs)
            else:
                return redirect('login')
        return wrapper
    return decorator