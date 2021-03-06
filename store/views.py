from urllib import request
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action  # APIView #api_view for function based views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, \
                                  RetrieveModelMixin, \
                                  UpdateModelMixin, \
                                  DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny                                  
# from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


from store.filters import ProductFilter
from store.pagination import DefaultPagination
from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistory
# from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import Cart, CartItem, Collection, Customer, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, \
                         CartItemSerializer, CustomerSerializer, \
                         UpdateCartItemSerializer, \
                         CartSerializer, \
                         CollectionSerializer, \
                         ProductSerializer, \
                         ReviewSerializer
from store import serializers



# generic view set for product resource
class ProductViewSet(ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class =  DefaultPagination   #PageNumberPagination  #already set in settings 
    permission_classes = [IsAdminOrReadOnly]
    # filterset_fields = ['collection_id', 'unit_price']

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')

        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)

        return queryset

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count>0:
           return Response(
                        {'error': 'cant delete.. it belongs to some order'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return super().destroy(request, *args, **kwargs)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=id)    #Product.objects.get(pk=id)
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


# generic API viewset for Collection 
class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        return Collection.objects.annotate(
            products_count=Count('products')
        ).all()

    def get_serializer_class(self):
        return CollectionSerializer

    def get_serializer_context(self):
        return {'request': request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count>0:
            return Response(
                        {'error': 'cant delete.. it belongs to some order'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    
    #     if collection.products.count()>0:
    #         return Response({'error': 'Can not delete: Not empty'}, status=status.HTTP_400_BAD_REQUEST)

    #     collection.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

 
class ReviewViewSet(ModelViewSet):

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['products_pk'])

    def get_serializer_class(self):
        return ReviewSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}



class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        return CartSerializer



class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'put', 'post', 'delete']
    
    def get_queryset(self):
        return CartItem.objects.select_related('products').filter(cart_id=self.kwargs['cart_pk'])  
                
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer

        elif request.method=='PATCH':
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
 


class CustomerViewSet(ModelViewSet): #CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    
    permission_classes =  [IsAdminUser]  # [FullDjangoModelPermissions]
    def get_queryset(self):
        return Customer.objects.all()

    def get_serializer_class(self):
        return CustomerSerializer

    
    def get_permissions(self):
        if request.method=='GET':
            return [AllowAny()]

        return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistory])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)  #anonymous

        if request.method=='GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method=='PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
             






# generic API view
# class ProductList(ListCreateAPIView):

#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def get_serializer_context(self):
#         return {'request': request}

    
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer=ProductSerializer(data=request.data)
        
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # serializer.validated_data
    #     return Response('ok')


# class ProductDetail(RetrieveUpdateDestroyAPIView):

#     # lookup_field='id'

#     def get_queryset(self):
#         return Product.objects.all()

#     def get_serializer_class(self):
#         return ProductSerializer

    # customizing the delete method in RetrieveUpdateDeleteAPIView
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=id)    #Product.objects.get(pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)    #Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)    #Product.objects.get(pk=id)
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid()
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)



 

# generic api view for collection list api
# class CollectionList(ListCreateAPIView):

#     def get_queryset(self):
#         return Collection.objects.annotate(
#             products_count=Count('products')).all()

#     def get_serializer_class(self):
#         return CollectionSerializer

#     def get_serializer_context(self):
#         return {'request': request}


# class CollectionDetail(RetrieveUpdateDestroyAPIView):

#     def get_queryset(self):
#         return Collection.objects.annotate(products_count=Count('products'))


#     def get_serializer_class(self):
#         return CollectionSerializer

    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    
    #     if collection.products.coun t()>0:
    #         return Response({'error': 'Can not delete: Not empty'}, status=status.HTTP_400_BAD_REQUEST)

    #     collection.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)
 




