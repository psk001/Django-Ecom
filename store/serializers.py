from decimal import Decimal
from itertools import product
from math import prod
from pyexpat import model
from statistics import mode
from xml.sax.handler import property_declaration_handler
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model= Product   #for relations it uses PrimaryKeyRealtedField
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
                    # '__all__' if all fields are to be included

    # id = serializers.IntegerField() 
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection =  serializers.HyperlinkedRelatedField(
    #                 queryset=Collection.objects.all(),
    #                 view_name='collection-detail'  )  #gives hyperlink
                  # CollectionSerializer() 
                  # serializers.StringRelatedField( queryset=Collection.objects.all() )
                  # serializers.PrimaryKeyRelatedField()

    def calculate_tax(self, product:Product):
        return product.unit_price*Decimal(1.2)

    # BUILT IN METHODS

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError()

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.some_field=2
    #     product.save()
    #     return product #super().create(validated_data)

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'review']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create (product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model=CartItem
        fields=['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):   #doubt
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model=Cart
        fields=['id', 'items', 'total_price']
 

class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product found')
        
        return value 

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']






