from django.shortcuts import render
from django.shortcuts import redirect, render


def index(request):
    return render(request, "nshop/index.html")

def login(request):
    return render(request, "nshop/login.html")

def register(request):
    return render(request, "nshop/register.html")

def add_item(request):
    return render(request, "nshop/add.html")