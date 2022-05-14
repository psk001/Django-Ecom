from decimal import Decimal
from math import prod
from pyexpat import model
from rest_framework import serializers
from .models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField()


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

















