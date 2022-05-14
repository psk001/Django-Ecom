from types import MemberDescriptorType
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import Q, F, Func, Count
from store.models import Customer

# Create your views here.

#@transaction.atomic()
def say_hello(request):
    #look up types in field
    #query_set= Customer.objects.filter(membership='BR')  #exists()    #first()  #.get(pk=1) primary key 
    
    #using connection
    # with connection.cursor() as cursor:
    #     cursor.execute('query')    

    # with transaction.atomic():
    query_set = Customer.objects.filter(Q(membership='BR') | Q(membership='SL'))
    
    #raw sql queries
    #queryset=Customer.objects.raw('query')

    # fields
    #query_set = Customer.objects.values('id', 'first_name') # sends dictionaries
    
    # fields
    #query_set = Customer.objects.values_list('id', 'first_name') # sends tuples

    #asc
    #query_set = Customer.objects.earliest(Q(membership='BR') | Q(membership='SL'))
    
    #desc
    #query_set = Customer.objects.latest(Q(membership='BR') | Q(membership='SL'))
    
    return render(
                request, 
                'hello.html',
                {
                    'name':'psk',
                    'products': list(query_set)
                },
            )                 #HttpResponse('hello world')
