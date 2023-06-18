from .models import Customer
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

def create_customer(sender,instance,created,**kwargs):
    if created:
        group=Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance,name=instance.username)
        print("User created successfully")


post_save.connect(create_customer,sender=User)