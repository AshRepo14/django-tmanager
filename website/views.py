from django.shortcuts import render

from api.models import Item


def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def user_operations(request):
    return render(request, 'operation.html')

def register(request):
    return render(request, 'register.html')
    
def login(request):
    return render(request, 'login.html')

def operation(request):
    return render(request, 'operation.html')

def user(request):
    return render(request, 'user.html')
