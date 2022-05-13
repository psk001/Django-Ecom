from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def calc():
    x=1
    y=2

    return x

def say_hello(request):
    x=calc()
    return render(
                request, 
                'hello.html',
                {'name':'psk'}
            )                 #HttpResponse('hello world')
