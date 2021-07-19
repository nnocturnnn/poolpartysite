from django.shortcuts import render
from django.shortcuts import redirect, render

def index(request):
    return render(request, "nshop/index.html")

def login(request):
    return render(request, "nshop/login.html")
