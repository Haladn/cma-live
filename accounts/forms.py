from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order,Customer

class Orderform(ModelForm):
    class Meta:
        model=Order
        fields="__all__"

class Createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class Customerform(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']
