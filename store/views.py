from http.client import SERVICE_UNAVAILABLE
from re import S
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method=='GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data
        return Response('ok')


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)    #Product.objects.get(pk=id)
    
    if request.method == 'GET':             
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method=='DELETE':
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method=='GET':
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method=='POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Ok')

    

@api_view(['GET', 'POST', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
                        Collection.objects.annotate(products_count=Count('products')), 
                        pk=pk
                    )

    if request.method=='GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method=='PUT':
        serializer= CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    elif request.method=='DELETE':
        if collection.products.count()>0:
            return Response({'error': 'Can not delete: Not empty'}, status=status.HTTP_400_BAD_REQUEST)

        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
 




