from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib import admin
from uuid import uuid4

from store import permissions


# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #product_set comes from many to many field from products

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
                                    'Product', 
                                    on_delete=models.SET_NULL, 
                                    related_name='+',
                                    null=True
                                )

    def  __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion)

    def  __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBER_BRONZE='BR'
    MEMBER_SILVER='SL'
    MEMBER_GOLD='GL'

    MEMBER_TYPES = [
        (MEMBER_BRONZE, 'Bronze'),
        (MEMBER_SILVER, 'Silver'),
        (MEMBER_GOLD, 'Gold')
    ]

    # first_name= models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=2, 
                                  choices=MEMBER_TYPES, 
                                  default=MEMBER_BRONZE
                                )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def  __str__(self):
        return self.user.first_name + " " + self.user.last_name

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

class Order(models.Model):
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'

    PAYMENT_STATUS= [  
            (PAYMENT_STATUS_PENDING, 'Pending'),
            (PAYMENT_STATUS_COMPLETE, 'Complete'),
            (PAYMENT_STATUS_FAILED, 'Failed')
        ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
                                    max_length=1,
                                    choices= PAYMENT_STATUS,
                                    default=PAYMENT_STATUS_PENDING   
                                )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    #custom permissions 
    class Meta:
        permissions = [
            ('cancel_order', 'can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    zipcode = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
                            Customer, 
                            on_delete=models.CASCADE
                        )


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)



                
