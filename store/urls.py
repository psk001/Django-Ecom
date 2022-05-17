from cgitb import lookup
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
# from rest_framework_nested import routers
from . import views

router =  DefaultRouter()           # SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet, basename='collections')

# prodcuts_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# prodcuts_router.register('reviews', views.ReviewViewSet, basename='product-reviews')



# routes set from router,urls
urlpatterns = router.urls  #+ prodcuts_router

#url conf module
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
