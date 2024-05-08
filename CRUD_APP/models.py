from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import time

# Create your models here.

userchoices={
    (1,"ADMIN"),
    # (2,"EMPLOYEE"),
    (3,"CLIENT")
}


class User(AbstractUser):
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ['phone_number','username']
    name = models.CharField(max_length=255,null=True,blank=True)
    user_type = models.IntegerField(default=1, choices=userchoices)
    phone_number = models.CharField(max_length=13,null=True,blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # staff_id=models.CharField(max_length=13,unique=True,null=True)

class Item(models.Model):
    itemcode = models.CharField(max_length=255,null=True,blank=True)
    itemname = models.CharField(max_length=255,null=True,blank=True)
    itemdescription=models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category= models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.itemname


class Address(models.Model):
    city = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    zip_code = models.CharField(max_length=255,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'Cancelled'),
        (1, 'New'),
        (2, 'Pending'),
        (3, 'Delivered'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    # order_number = models.CharField(max_length=10, unique=True, default='000000')

    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    quantity = models.IntegerField(default=1)


    


 


