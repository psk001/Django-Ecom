from ast import Or
from enum import auto
from gc import collect
from http.client import PAYMENT_REQUIRED
from math import prod
from platform import release
from statistics import mode
from django.db import models


# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #product_set comes from many to many field from products

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_products = models.ForeignKey(
                                    'Product', 
                                    on_delete=models.SET_NULL, 
                                    related_name='+',
                                    null=True
                                )


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBER_BRONZE='BR'
    MEMBER_SILVER='SL'
    MEMBER_GOLD='GL'

    MEMBER_TYPES = [
        (MEMBER_BRONZE, 'Bronze'),
        (MEMBER_SILVER, 'Silver'),
        (MEMBER_GOLD, 'Gold')
    ]

    first_name= models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=2, 
                                  choices=MEMBER_TYPES, 
                                  default=MEMBER_BRONZE
                                )


class Order(models.Model):
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'

    PAYMENT_STATUS= [  
            (PAYMENT_STATUS_PENDING, 'Pending'),
            (PAYMENT_STATUS_COMPLETE, 'Complete'),
            (PAYMENT_STATUS_FAILED, 'Failed')
        ]
    plcaed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
                                    max_length=1,
                                    choices= PAYMENT_STATUS,
                                    default=PAYMENT_STATUS_PENDING   
                                )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
                            Customer, 
                            on_delete=models.CASCADE
                        )


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()







                
